"""
SARS-CoV-2
==========

Data Source: WashU Virus Genome Browser, NCBI, GISAID
"""
# category: others
import gosling as gos

gene_data = gos.csv(
    url="https://s3.amazonaws.com/gosling-lang.org/data/COVID/NC_045512.2-Genes.csv",
    chromosomeField="Accession",
    genomicFields=["Start", "Stop"],
)

genes_base = gos.Track(gene_data).encode(
    x=gos.X("Start:G"),
    xe=gos.Xe("Stop:G"),
).properties(
    width=800,
    height=30,
)


genes = gos.overlay(
    genes_base.mark_rect().encode(
        color=gos.value("#0072B2"),
        stroke=gos.value("white"),
        strokeWidth=gos.value(2),
    ),
    genes_base.mark_rule(linePattern=dict(type="triangleRight", size=10)).encode(
        color=gos.value("white"),
        opacity=gos.value(0.6),
        strokeWidth=gos.value(0),
    ),
    genes_base.mark_text().encode(
        text=gos.Text("Gene symbol:N"),
        color=gos.value("black"),
        stroke=gos.value("white"),
        strokeWidth=gos.value(3),
    ).visibility_le(
        target="mark",
        measure="width",
        threshold="|xe-x|",
        transitionPadding=30,
    ),
).properties(
    title="NC_045512.2 Genes",
)

protein_data = gos.csv(
    url="https://s3.amazonaws.com/gosling-lang.org/data/COVID/sars-cov-2_Sprot_annot_sorted.bed",
    chromosomeField="Accession",
    genomicFields=["Start", "Stop"],
)

domain = [
    "receptor-binding domain (RBD)",
    "receptor-binding motif (RBM)",
    "S1/S2 cleavage site",
    "heptad repeat 1 (HR1)",
    "heptad repeat 2 (HR2)",
]

proteins_base = gos.Track(protein_data).encode(
    x=gos.X("Start:G"),
    row=gos.Row("Protein:N", domain=domain),
).properties(
    width=800,
    height=80,
)

proteins = gos.overlay(
    proteins_base.mark_rect().encode(
        color=gos.Color("Protein:N", domain=domain),
        xe=gos.Xe("Stop:G"),
    ),
    proteins_base.mark_text(textAnchor="end").encode(
        text=gos.Text("Protein:N"),
        color=gos.value("#333"),
        stroke=gos.value("white"),
        strokeWidth=gos.value(3),
    ),
).properties(
    title="S Protein Annotation",
)

recomb_data = gos.csv(
    url="https://s3.amazonaws.com/gosling-lang.org/data/COVID/TRS-L-dependent_recombinationEvents_sorted.bed",
    chromosomeField="Accession",
    genomicFields=["Start1", "Stop1", "Start2", "Stop2"],
    sampleLength=100,
)

recomb = gos.Track(recomb_data).mark_withinLink().encode(
    x=gos.X("Start1:G"),
    xe=gos.Xe("Stop1:G"),
    x1=gos.X1("Start2:G"),
    x1e=gos.X1e("Stop2:G"),
    stroke=gos.value("#0072B2"),
    color=gos.value("#0072B2"),
    opacity=gos.value(0.1),
).properties(
    title="TRS-L-Dependent Recombination Events",
    width=800,
    height=400,
)

gos.stack(genes, proteins, recomb).properties(
    assembly=[["NC_045512.2", 29903]],
    xDomain=gos.DomainInterval([1, 29903]),
)
