"""
Between Links Using Pandas
==========================
"""
# category: skip
import gosling as gos
import pandas as pd

"""
Data Transform Using Pandas
"""
df = pd.read_csv(
    "https://raw.githubusercontent.com/vigsterkr/circos/master/data/5/segdup.txt", 
    sep=" ",
    header=0,
    names=["id", "chr", "start", "end"]
)

# Use chromosome names that are interpretable in gos
df.chr = df.chr.apply(lambda x: x.replace("hs", "chr"))

# Select ids that occur exact two times
df = df[df.groupby("id")["id"].transform("size") == 2]

# Long to wide (i.e., "chr, start, end" --> "first_chr, first_start, first_end, second_chr, second_start, second_end")
df["cumcnt"] = df.groupby("id").cumcount()
df = pd.DataFrame(df.pivot(index="id", columns="cumcnt")[["chr", "start", "end"]].to_records())
df = df.rename(columns={
    "('chr', 0)": "first_chr", 
    "('chr', 1)": "second_chr", 
    "('start', 0)": "first_start", 
    "('start', 1)": "second_start", 
    "('end', 0)": "first_end", 
    "('end', 1)": "second_end"
})

df_bg = df[(df.first_chr == 'chr1') | (df.second_chr == 'chr1')]
df_hl = df[(df.first_chr != 'chr1') & (df.second_chr != 'chr1')]

column_info = [
    {"chromosomeField": "first_chr", "genomicFields": ["first_start", "first_end"]}, 
    {"chromosomeField": "second_chr", "genomicFields": ["second_start", "second_end"]}
]
data_bg = df_bg.gos.csv(genomicFieldsToConvert=column_info)
data_hl = df_hl.gos.csv(genomicFieldsToConvert=column_info)

"""
Encoding
"""
def set_encoding(track):
    return track.mark_withinLink().encode(
        x=gos.X("first_start:G"),
        xe=gos.Xe("second_end:G"),
        opacity=gos.value(0.2)
    )

gos.overlay(
    set_encoding(gos.Track(data_bg)).encode(stroke=gos.value("lightgray")),
    set_encoding(gos.Track(data_hl)).encode(stroke=gos.Stroke("second_chr:N"))
).properties(
    width=600,
    height=200
)
