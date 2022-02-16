# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly.

from gosling.schemapi import SchemaBase, Undefined, _subclasses

import pkgutil
import json

def load_schema():
    """Load the json schema associated with this module's functions"""
    return json.loads(pkgutil.get_data(__name__, 'gosling-schema.json').decode('utf-8'))


class GoslingSchema(SchemaBase):
    _rootschema = load_schema()
    @classmethod
    def _default_wrapper_classes(cls):
        return _subclasses(GoslingSchema)


class Root(GoslingSchema):
    """Root schema wrapper

    anyOf(:class:`RootSpecWithSingleView`, :class:`RootSpecWithMultipleViews`)
    """
    _schema = GoslingSchema._rootschema
    _rootschema = _schema

    def __init__(self, *args, **kwds):
        super(Root, self).__init__(*args, **kwds)


class Aggregate(GoslingSchema):
    """Aggregate schema wrapper

    enum('max', 'min', 'mean', 'bin', 'count')
    """
    _schema = {'$ref': '#/definitions/Aggregate'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(Aggregate, self).__init__(*args)


class Assembly(GoslingSchema):
    """Assembly schema wrapper

    enum('hg38', 'hg19', 'hg18', 'hg17', 'hg16', 'mm10', 'mm9', 'unknown')
    """
    _schema = {'$ref': '#/definitions/Assembly'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(Assembly, self).__init__(*args)


class AxisPosition(GoslingSchema):
    """AxisPosition schema wrapper

    enum('none', 'top', 'bottom', 'left', 'right')
    """
    _schema = {'$ref': '#/definitions/AxisPosition'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(AxisPosition, self).__init__(*args)


class BinAggregate(GoslingSchema):
    """BinAggregate schema wrapper

    enum('mean', 'sum')
    """
    _schema = {'$ref': '#/definitions/BinAggregate'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(BinAggregate, self).__init__(*args)


class Channel(GoslingSchema):
    """Channel schema wrapper

    anyOf(:class:`ChannelDeep`, :class:`ChannelValue`)
    """
    _schema = {'$ref': '#/definitions/Channel'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Channel, self).__init__(*args, **kwds)


class ChannelDeep(Channel):
    """ChannelDeep schema wrapper

    anyOf(:class:`X`, :class:`Y`, :class:`Row`, :class:`Color`, :class:`Size`, :class:`Stroke`,
    :class:`StrokeWidth`, :class:`Opacity`, :class:`Text`)
    """
    _schema = {'$ref': '#/definitions/ChannelDeep'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(ChannelDeep, self).__init__(*args, **kwds)


class ChannelValue(Channel):
    """ChannelValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _schema = {'$ref': '#/definitions/ChannelValue'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, value=Undefined, **kwds):
        super(ChannelValue, self).__init__(value=value, **kwds)


class Chromosome(GoslingSchema):
    """Chromosome schema wrapper

    enum('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
    '17', '18', '19', '20', '21', '22', 'X', 'Y', 'M', 'chr1', 'chr2', 'chr3', 'chr4', 'chr5',
    'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15',
    'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM')
    """
    _schema = {'$ref': '#/definitions/Chromosome'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(Chromosome, self).__init__(*args)


class Color(ChannelDeep):
    """Color schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    legend : boolean
        Whether to display legend. __Default__: `false`
    range : :class:`Range`
        Determine the colors that should be bound to data value. Default properties are
        determined considering the field type.
    scale : enum('linear', 'log')

    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/Color'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, legend=Undefined, range=Undefined,
                 scale=Undefined, type=Undefined, **kwds):
        super(Color, self).__init__(domain=domain, field=field, legend=legend, range=range, scale=scale,
                                    type=type, **kwds)


class DataDeep(GoslingSchema):
    """DataDeep schema wrapper

    anyOf(:class:`JSONData`, :class:`CSVData`, :class:`BIGWIGData`, :class:`MultivecData`,
    :class:`BEDDBData`, :class:`VectorData`, :class:`MatrixData`, :class:`BAMData`)
    """
    _schema = {'$ref': '#/definitions/DataDeep'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(DataDeep, self).__init__(*args, **kwds)


class BAMData(DataDeep):
    """BAMData schema wrapper

    Mapping(required=[type, url, indexUrl])
    Binary Alignment Map (BAM) is the comprehensive raw data of genome sequencing; it consists
    of the lossless, compressed binary representation of the Sequence Alignment Map-files.

    Attributes
    ----------

    indexUrl : string
        URL link to the index file of the BAM file
    type : string

    url : string
        URL link to the BAM data file
    extractJunction : boolean
        Determine whether to extract exon-to-exon junctions. __Default__: `false`
    junctionMinCoverage : float
        Determine the threshold of coverage when extracting exon-to-exon junctions.
        __Default__: `1`
    loadMates : boolean
        Load mates that are located in the same chromosome. __Default__: `false`
    maxInsertSize : float
        Determines the threshold of insert sizes for determining the structural variants.
        __Default__: `5000`
    """
    _schema = {'$ref': '#/definitions/BAMData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, indexUrl=Undefined, type=Undefined, url=Undefined, extractJunction=Undefined,
                 junctionMinCoverage=Undefined, loadMates=Undefined, maxInsertSize=Undefined, **kwds):
        super(BAMData, self).__init__(indexUrl=indexUrl, type=type, url=url,
                                      extractJunction=extractJunction,
                                      junctionMinCoverage=junctionMinCoverage, loadMates=loadMates,
                                      maxInsertSize=maxInsertSize, **kwds)


class BEDDBData(DataDeep):
    """BEDDBData schema wrapper

    Mapping(required=[type, url, genomicFields])
    Regular BED or similar files can be pre-aggregated for the scalable data exploration. Find
    our more about this format at [HiGlass
    Docs](https://docs.higlass.io/data_preparation.html#bed-files).

    Attributes
    ----------

    genomicFields : List(Mapping(required=[index, name]))
        Specify the name of genomic data fields.
    type : string

    url : string
        Specify the URL address of the data file.
    exonIntervalFields : List([Mapping(required=[index, name]), Mapping(required=[index,
    name])])
        experimental
    valueFields : List(Mapping(required=[index, name, type]))
        Specify the column indexes, field names, and field types.
    """
    _schema = {'$ref': '#/definitions/BEDDBData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, genomicFields=Undefined, type=Undefined, url=Undefined,
                 exonIntervalFields=Undefined, valueFields=Undefined, **kwds):
        super(BEDDBData, self).__init__(genomicFields=genomicFields, type=type, url=url,
                                        exonIntervalFields=exonIntervalFields, valueFields=valueFields,
                                        **kwds)


class BIGWIGData(DataDeep):
    """BIGWIGData schema wrapper

    Mapping(required=[type, url, column, value])

    Attributes
    ----------

    column : string
        Assign a field name of the middle position of genomic intervals.
    type : string

    url : string
        Specify the URL address of the data file.
    value : string
        Assign a field name of quantitative values.
    aggregation : :class:`BinAggregate`
        Determine aggregation function to apply within bins. __Default__: `"mean"`
    binSize : float
        Binning the genomic interval in tiles (unit size: 256).
    end : string
        Assign a field name of the end position of genomic intervals.
    start : string
        Assign a field name of the start position of genomic intervals.
    """
    _schema = {'$ref': '#/definitions/BIGWIGData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, column=Undefined, type=Undefined, url=Undefined, value=Undefined,
                 aggregation=Undefined, binSize=Undefined, end=Undefined, start=Undefined, **kwds):
        super(BIGWIGData, self).__init__(column=column, type=type, url=url, value=value,
                                         aggregation=aggregation, binSize=binSize, end=end, start=start,
                                         **kwds)


class CSVData(DataDeep):
    """CSVData schema wrapper

    Mapping(required=[type, url])
    Any small enough tabular data files, such as tsv, csv, BED, BEDPE, and GFF, can be loaded
    using "csv" data specification.

    Attributes
    ----------

    type : string

    url : string
        Specify the URL address of the data file.
    chromosomeField : string
        Specify the name of chromosome data fields.
    chromosomePrefix : string
        experimental
    genomicFields : List(string)
        Specify the name of genomic data fields.
    genomicFieldsToConvert : List(Mapping(required=[chromosomeField, genomicFields]))
        experimental
    headerNames : List(string)
        Specify the names of data fields if a CSV file is headerless.
    longToWideId : string
        experimental
    sampleLength : float
        Specify the number of rows loaded from the URL.

        __Default:__ `1000`
    separator : string
        Specify file separator, __Default:__ ','
    """
    _schema = {'$ref': '#/definitions/CSVData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, url=Undefined, chromosomeField=Undefined,
                 chromosomePrefix=Undefined, genomicFields=Undefined, genomicFieldsToConvert=Undefined,
                 headerNames=Undefined, longToWideId=Undefined, sampleLength=Undefined,
                 separator=Undefined, **kwds):
        super(CSVData, self).__init__(type=type, url=url, chromosomeField=chromosomeField,
                                      chromosomePrefix=chromosomePrefix, genomicFields=genomicFields,
                                      genomicFieldsToConvert=genomicFieldsToConvert,
                                      headerNames=headerNames, longToWideId=longToWideId,
                                      sampleLength=sampleLength, separator=separator, **kwds)


class DataTransform(GoslingSchema):
    """DataTransform schema wrapper

    anyOf(:class:`FilterTransform`, :class:`StrConcatTransform`, :class:`StrReplaceTransform`,
    :class:`LogTransform`, :class:`DisplaceTransform`, :class:`ExonSplitTransform`,
    :class:`GenomicLengthTransform`, :class:`CoverageTransform`, :class:`JSONParseTransform`)
    """
    _schema = {'$ref': '#/definitions/DataTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(DataTransform, self).__init__(*args, **kwds)


class CoverageTransform(DataTransform):
    """CoverageTransform schema wrapper

    Mapping(required=[type, startField, endField])
    Aggregate rows and calculate coverage

    Attributes
    ----------

    endField : string

    startField : string

    type : string

    groupField : string
        The name of a nominal field to group rows by in prior to piling-up
    newField : string

    """
    _schema = {'$ref': '#/definitions/CoverageTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, endField=Undefined, startField=Undefined, type=Undefined, groupField=Undefined,
                 newField=Undefined, **kwds):
        super(CoverageTransform, self).__init__(endField=endField, startField=startField, type=type,
                                                groupField=groupField, newField=newField, **kwds)


class Datum(GoslingSchema):
    """Datum schema wrapper

    Mapping(required=[])
    Values in the form of JSON.
    """
    _schema = {'$ref': '#/definitions/Datum'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, **kwds):
        super(Datum, self).__init__(**kwds)


class DisplaceTransform(DataTransform):
    """DisplaceTransform schema wrapper

    Mapping(required=[type, boundingBox, method, newField])

    Attributes
    ----------

    boundingBox : Mapping(required=[startField, endField])

    method : :class:`DisplacementType`
        A string that specifies the type of diseplancement.
    newField : string

    type : string

    maxRows : float
        Specify maximum rows to be generated (default has no limit).
    """
    _schema = {'$ref': '#/definitions/DisplaceTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, boundingBox=Undefined, method=Undefined, newField=Undefined, type=Undefined,
                 maxRows=Undefined, **kwds):
        super(DisplaceTransform, self).__init__(boundingBox=boundingBox, method=method,
                                                newField=newField, type=type, maxRows=maxRows, **kwds)


class Displacement(GoslingSchema):
    """Displacement schema wrapper

    Mapping(required=[type])

    Attributes
    ----------

    type : :class:`DisplacementType`

    padding : float

    """
    _schema = {'$ref': '#/definitions/Displacement'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, padding=Undefined, **kwds):
        super(Displacement, self).__init__(type=type, padding=padding, **kwds)


class DisplacementType(GoslingSchema):
    """DisplacementType schema wrapper

    enum('pile', 'spread')
    """
    _schema = {'$ref': '#/definitions/DisplacementType'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(DisplacementType, self).__init__(*args)


class ExonSplitTransform(DataTransform):
    """ExonSplitTransform schema wrapper

    Mapping(required=[type, separator, flag, fields])

    Attributes
    ----------

    fields : List(Mapping(required=[field, type, newField, chrField]))

    flag : Mapping(required=[field, value])

    separator : string

    type : string

    """
    _schema = {'$ref': '#/definitions/ExonSplitTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, fields=Undefined, flag=Undefined, separator=Undefined, type=Undefined, **kwds):
        super(ExonSplitTransform, self).__init__(fields=fields, flag=flag, separator=separator,
                                                 type=type, **kwds)


class FieldType(GoslingSchema):
    """FieldType schema wrapper

    enum('genomic', 'nominal', 'quantitative')
    """
    _schema = {'$ref': '#/definitions/FieldType'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(FieldType, self).__init__(*args)


class FilterTransform(DataTransform):
    """FilterTransform schema wrapper

    anyOf(:class:`OneOfFilter`, :class:`RangeFilter`, :class:`IncludeFilter`)
    """
    _schema = {'$ref': '#/definitions/FilterTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(FilterTransform, self).__init__(*args, **kwds)


class GenomicDomain(GoslingSchema):
    """GenomicDomain schema wrapper

    anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`,
    :class:`DomainGene`)
    """
    _schema = {'$ref': '#/definitions/GenomicDomain'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(GenomicDomain, self).__init__(*args, **kwds)


class DomainChr(GenomicDomain):
    """DomainChr schema wrapper

    Mapping(required=[chromosome])

    Attributes
    ----------

    chromosome : :class:`Chromosome`

    """
    _schema = {'$ref': '#/definitions/DomainChr'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, chromosome=Undefined, **kwds):
        super(DomainChr, self).__init__(chromosome=chromosome, **kwds)


class DomainChrInterval(GenomicDomain):
    """DomainChrInterval schema wrapper

    Mapping(required=[chromosome, interval])

    Attributes
    ----------

    chromosome : :class:`Chromosome`
        If specified, only showing a certain interval in a chromosome.
    interval : List([float, float])

    """
    _schema = {'$ref': '#/definitions/DomainChrInterval'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, chromosome=Undefined, interval=Undefined, **kwds):
        super(DomainChrInterval, self).__init__(chromosome=chromosome, interval=interval, **kwds)


class DomainGene(GenomicDomain):
    """DomainGene schema wrapper

    Mapping(required=[gene])

    Attributes
    ----------

    gene : anyOf(string, List([string, string]))

    """
    _schema = {'$ref': '#/definitions/DomainGene'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, gene=Undefined, **kwds):
        super(DomainGene, self).__init__(gene=gene, **kwds)


class DomainInterval(GenomicDomain):
    """DomainInterval schema wrapper

    Mapping(required=[interval])

    Attributes
    ----------

    interval : List([float, float])

    """
    _schema = {'$ref': '#/definitions/DomainInterval'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, interval=Undefined, **kwds):
        super(DomainInterval, self).__init__(interval=interval, **kwds)


class GenomicLengthTransform(DataTransform):
    """GenomicLengthTransform schema wrapper

    Mapping(required=[type, startField, endField, newField])
    Calculate genomic length using two genomic fields

    Attributes
    ----------

    endField : string

    newField : string

    startField : string

    type : string

    """
    _schema = {'$ref': '#/definitions/GenomicLengthTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, endField=Undefined, newField=Undefined, startField=Undefined, type=Undefined,
                 **kwds):
        super(GenomicLengthTransform, self).__init__(endField=endField, newField=newField,
                                                     startField=startField, type=type, **kwds)


class GoslingSpec(GoslingSchema):
    """GoslingSpec schema wrapper

    anyOf(:class:`RootSpecWithSingleView`, :class:`RootSpecWithMultipleViews`)
    """
    _schema = {'$ref': '#/definitions/GoslingSpec'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(GoslingSpec, self).__init__(*args, **kwds)


class IncludeFilter(FilterTransform):
    """IncludeFilter schema wrapper

    Mapping(required=[field, include, type])

    Attributes
    ----------

    field : string
        A filter is applied based on the values of the specified data field
    include : string
        Check whether the value includes a substring.
    type : string

    not : boolean
        when `{"not": true}`, apply a NOT logical operation to the filter.

        __Default:__ `false`
    """
    _schema = {'$ref': '#/definitions/IncludeFilter'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, include=Undefined, type=Undefined, **kwds):
        super(IncludeFilter, self).__init__(field=field, include=include, type=type, **kwds)


class JSONData(DataDeep):
    """JSONData schema wrapper

    Mapping(required=[type, values])
    The JSON data format allows users to include data directly in the Gosling's JSON
    specification.

    Attributes
    ----------

    type : string
        Define data type.
    values : List(:class:`Datum`)
        Values in the form of JSON.
    chromosomeField : string
        Specify the name of chromosome data fields.
    genomicFields : List(string)
        Specify the name of genomic data fields.
    genomicFieldsToConvert : List(Mapping(required=[chromosomeField, genomicFields]))
        experimental
    sampleLength : float
        Specify the number of rows loaded from the URL.

        __Default:__ `1000`
    """
    _schema = {'$ref': '#/definitions/JSONData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, values=Undefined, chromosomeField=Undefined,
                 genomicFields=Undefined, genomicFieldsToConvert=Undefined, sampleLength=Undefined,
                 **kwds):
        super(JSONData, self).__init__(type=type, values=values, chromosomeField=chromosomeField,
                                       genomicFields=genomicFields,
                                       genomicFieldsToConvert=genomicFieldsToConvert,
                                       sampleLength=sampleLength, **kwds)


class JSONParseTransform(DataTransform):
    """JSONParseTransform schema wrapper

    Mapping(required=[type, field, baseGenomicField, genomicField, genomicLengthField])
    Parse JSON Object Array and append vertically

    Attributes
    ----------

    baseGenomicField : string
        Base genomic position when parsing relative position.
    field : string
        The field that contains the JSON object array.
    genomicField : string
        Relative genomic position to parse.
    genomicLengthField : string
        Length of genomic interval.
    type : string

    """
    _schema = {'$ref': '#/definitions/JSONParseTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, baseGenomicField=Undefined, field=Undefined, genomicField=Undefined,
                 genomicLengthField=Undefined, type=Undefined, **kwds):
        super(JSONParseTransform, self).__init__(baseGenomicField=baseGenomicField, field=field,
                                                 genomicField=genomicField,
                                                 genomicLengthField=genomicLengthField, type=type,
                                                 **kwds)


class Layout(GoslingSchema):
    """Layout schema wrapper

    enum('linear', 'circular')
    """
    _schema = {'$ref': '#/definitions/Layout'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(Layout, self).__init__(*args)


class LogBase(GoslingSchema):
    """LogBase schema wrapper

    anyOf(float, string)
    """
    _schema = {'$ref': '#/definitions/LogBase'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(LogBase, self).__init__(*args, **kwds)


class LogTransform(DataTransform):
    """LogTransform schema wrapper

    Mapping(required=[type, field])

    Attributes
    ----------

    field : string

    type : string

    base : :class:`LogBase`
        If not specified, 10 is used.
    newField : string
        If specified, store transformed values in a new field.
    """
    _schema = {'$ref': '#/definitions/LogTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, type=Undefined, base=Undefined, newField=Undefined, **kwds):
        super(LogTransform, self).__init__(field=field, type=type, base=base, newField=newField, **kwds)


class LogicalOperation(GoslingSchema):
    """LogicalOperation schema wrapper

    enum('less-than', 'lt', 'LT', 'greater-than', 'gt', 'GT', 'less-than-or-equal-to', 'ltet',
    'LTET', 'greater-than-or-equal-to', 'gtet', 'GTET')
    """
    _schema = {'$ref': '#/definitions/LogicalOperation'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(LogicalOperation, self).__init__(*args)


class Mark(GoslingSchema):
    """Mark schema wrapper

    enum('point', 'line', 'area', 'bar', 'rect', 'text', 'withinLink', 'betweenLink', 'rule',
    'triangleLeft', 'triangleRight', 'triangleBottom', 'brush', 'header')
    """
    _schema = {'$ref': '#/definitions/Mark'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(Mark, self).__init__(*args)


class MatrixData(DataDeep):
    """MatrixData schema wrapper

    Mapping(required=[type, url])

    Attributes
    ----------

    type : string

    url : string
        URL link to the matrix data file
    binSize : float
        Determine the number of nearby cells to aggregate. __Default__: `1`
    column : string
        The name of the first genomic field. __Default__: `x`
    row : string
        The name of the first genomic field. __Default__: `y`
    value : string
        The name of the value field. __Default__: `value`
    """
    _schema = {'$ref': '#/definitions/MatrixData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, url=Undefined, binSize=Undefined, column=Undefined,
                 row=Undefined, value=Undefined, **kwds):
        super(MatrixData, self).__init__(type=type, url=url, binSize=binSize, column=column, row=row,
                                         value=value, **kwds)


class MultipleViews(GoslingSchema):
    """MultipleViews schema wrapper

    Mapping(required=[views])

    Attributes
    ----------

    views : List(anyOf(:class:`SingleView`, :class:`MultipleViews`))
        An array of view specifications
    arrangement : enum('parallel', 'serial', 'horizontal', 'vertical')
        Specify how multiple views are arranged.
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    orientation : :class:`Orientation`
        Specify the orientation.
    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/MultipleViews'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, views=Undefined, arrangement=Undefined, assembly=Undefined,
                 centerRadius=Undefined, layout=Undefined, linkingId=Undefined, orientation=Undefined,
                 spacing=Undefined, static=Undefined, style=Undefined, xAxis=Undefined,
                 xDomain=Undefined, xOffset=Undefined, yDomain=Undefined, yOffset=Undefined,
                 zoomLimits=Undefined, **kwds):
        super(MultipleViews, self).__init__(views=views, arrangement=arrangement, assembly=assembly,
                                            centerRadius=centerRadius, layout=layout,
                                            linkingId=linkingId, orientation=orientation,
                                            spacing=spacing, static=static, style=style, xAxis=xAxis,
                                            xDomain=xDomain, xOffset=xOffset, yDomain=yDomain,
                                            yOffset=yOffset, zoomLimits=zoomLimits, **kwds)


class MultivecData(DataDeep):
    """MultivecData schema wrapper

    Mapping(required=[type, url, column, row, value])
    Two-dimensional quantitative values, one axis for genomic coordinate and the other for
    different samples, can be converted into HiGlass' `"multivec"` data. For example, multiple
    BigWig files can be converted into a single multivec file. You can also convert sequence
    data (FASTA) into this format where rows will be different nucleotide bases (e.g., A, T, G,
    C) and quantitative values represent the frequency. Find out more about this format at
    [HiGlass Docs](https://docs.higlass.io/data_preparation.html#multivec-files).

    Attributes
    ----------

    column : string
        Assign a field name of the middle position of genomic intervals.
    row : string
        Assign a field name of samples.
    type : string

    url : string
        Specify the URL address of the data file.
    value : string
        Assign a field name of quantitative values.
    aggregation : :class:`BinAggregate`
        Determine aggregation function to apply within bins. __Default__: `"mean"`
    binSize : float
        Binning the genomic interval in tiles (unit size: 256).
    categories : List(string)
        assign names of individual samples.
    end : string
        Assign a field name of the end position of genomic intervals.
    start : string
        Assign a field name of the start position of genomic intervals.
    """
    _schema = {'$ref': '#/definitions/MultivecData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, column=Undefined, row=Undefined, type=Undefined, url=Undefined, value=Undefined,
                 aggregation=Undefined, binSize=Undefined, categories=Undefined, end=Undefined,
                 start=Undefined, **kwds):
        super(MultivecData, self).__init__(column=column, row=row, type=type, url=url, value=value,
                                           aggregation=aggregation, binSize=binSize,
                                           categories=categories, end=end, start=start, **kwds)


class OneOfFilter(FilterTransform):
    """OneOfFilter schema wrapper

    Mapping(required=[field, oneOf, type])

    Attributes
    ----------

    field : string
        A filter is applied based on the values of the specified data field
    oneOf : anyOf(List(string), List(float))
        Check whether the value is an element in the provided list.
    type : string

    not : boolean
        when `{"not": true}`, apply a NOT logical operation to the filter.

        __Default:__ `false`
    """
    _schema = {'$ref': '#/definitions/OneOfFilter'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, oneOf=Undefined, type=Undefined, **kwds):
        super(OneOfFilter, self).__init__(field=field, oneOf=oneOf, type=type, **kwds)


class Opacity(ChannelDeep):
    """Opacity schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    range : :class:`ValueExtent`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/Opacity'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, range=Undefined, type=Undefined, **kwds):
        super(Opacity, self).__init__(domain=domain, field=field, range=range, type=type, **kwds)


class Orientation(GoslingSchema):
    """Orientation schema wrapper

    enum('horizontal', 'vertical')
    """
    _schema = {'$ref': '#/definitions/Orientation'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(Orientation, self).__init__(*args)


class PartialTrack(GoslingSchema):
    """PartialTrack schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    color : anyOf(:class:`Color`, :class:`ChannelValue`)

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    encoding : Mapping(required=[])

    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    flipY : boolean

    height : float
        Specify the track height in pixels.
    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    mark : :class:`Mark`

    opacity : anyOf(:class:`Opacity`, :class:`ChannelValue`)

    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlay : List(Mapping(required=[]))

    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])
        internal
    row : anyOf(:class:`Row`, :class:`ChannelValue`)

    size : anyOf(:class:`Size`, :class:`ChannelValue`)

    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    stretch : boolean

    stroke : anyOf(:class:`Stroke`, :class:`ChannelValue`)

    strokeWidth : anyOf(:class:`StrokeWidth`, :class:`ChannelValue`)

    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    template : string

    text : anyOf(:class:`Text`, :class:`ChannelValue`)

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    width : float
        Specify the track width in pixels.
    x : anyOf(:class:`X`, :class:`ChannelValue`)

    x1 : anyOf(:class:`X`, :class:`ChannelValue`)

    x1e : anyOf(:class:`X`, :class:`ChannelValue`)

    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    xe : anyOf(:class:`X`, :class:`ChannelValue`)

    y : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1 : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1e : anyOf(:class:`Y`, :class:`ChannelValue`)

    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    ye : anyOf(:class:`Y`, :class:`ChannelValue`)

    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/PartialTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, color=Undefined, data=Undefined, dataTransform=Undefined,
                 displacement=Undefined, encoding=Undefined, endAngle=Undefined, flipY=Undefined,
                 height=Undefined, id=Undefined, innerRadius=Undefined, layout=Undefined,
                 linkingId=Undefined, mark=Undefined, opacity=Undefined, orientation=Undefined,
                 outerRadius=Undefined, overlay=Undefined, overlayOnPreviousTrack=Undefined,
                 overrideTemplate=Undefined, prerelease=Undefined, row=Undefined, size=Undefined,
                 spacing=Undefined, startAngle=Undefined, static=Undefined, stretch=Undefined,
                 stroke=Undefined, strokeWidth=Undefined, style=Undefined, subtitle=Undefined,
                 template=Undefined, text=Undefined, title=Undefined, tooltip=Undefined,
                 visibility=Undefined, width=Undefined, x=Undefined, x1=Undefined, x1e=Undefined,
                 xAxis=Undefined, xDomain=Undefined, xOffset=Undefined, xe=Undefined, y=Undefined,
                 y1=Undefined, y1e=Undefined, yDomain=Undefined, yOffset=Undefined, ye=Undefined,
                 zoomLimits=Undefined, **kwds):
        super(PartialTrack, self).__init__(_invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                           assembly=assembly, centerRadius=centerRadius, color=color,
                                           data=data, dataTransform=dataTransform,
                                           displacement=displacement, encoding=encoding,
                                           endAngle=endAngle, flipY=flipY, height=height, id=id,
                                           innerRadius=innerRadius, layout=layout, linkingId=linkingId,
                                           mark=mark, opacity=opacity, orientation=orientation,
                                           outerRadius=outerRadius, overlay=overlay,
                                           overlayOnPreviousTrack=overlayOnPreviousTrack,
                                           overrideTemplate=overrideTemplate, prerelease=prerelease,
                                           row=row, size=size, spacing=spacing, startAngle=startAngle,
                                           static=static, stretch=stretch, stroke=stroke,
                                           strokeWidth=strokeWidth, style=style, subtitle=subtitle,
                                           template=template, text=text, title=title, tooltip=tooltip,
                                           visibility=visibility, width=width, x=x, x1=x1, x1e=x1e,
                                           xAxis=xAxis, xDomain=xDomain, xOffset=xOffset, xe=xe, y=y,
                                           y1=y1, y1e=y1e, yDomain=yDomain, yOffset=yOffset, ye=ye,
                                           zoomLimits=zoomLimits, **kwds)


class Range(GoslingSchema):
    """Range schema wrapper

    anyOf(:class:`ValueExtent`, :class:`PREDEFINED_COLORS`)
    """
    _schema = {'$ref': '#/definitions/Range'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Range, self).__init__(*args, **kwds)


class PREDEFINED_COLORS(Range):
    """PREDEFINED_COLORS schema wrapper

    enum('viridis', 'grey', 'spectral', 'warm', 'cividis', 'bupu', 'rdbu', 'hot', 'pink')
    """
    _schema = {'$ref': '#/definitions/PREDEFINED_COLORS'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(PREDEFINED_COLORS, self).__init__(*args)


class RangeFilter(FilterTransform):
    """RangeFilter schema wrapper

    Mapping(required=[field, inRange, type])

    Attributes
    ----------

    field : string
        A filter is applied based on the values of the specified data field
    inRange : List(float)
        Check whether the value is in a number range.
    type : string

    not : boolean
        when `{"not": true}`, apply a NOT logical operation to the filter.

        __Default:__ `false`
    """
    _schema = {'$ref': '#/definitions/RangeFilter'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, inRange=Undefined, type=Undefined, **kwds):
        super(RangeFilter, self).__init__(field=field, inRange=inRange, type=type, **kwds)


class ResponsiveSize(GoslingSchema):
    """ResponsiveSize schema wrapper

    anyOf(boolean, Mapping(required=[]))
    """
    _schema = {'$ref': '#/definitions/ResponsiveSize'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(ResponsiveSize, self).__init__(*args, **kwds)


class RootSpecWithMultipleViews(GoslingSpec):
    """RootSpecWithMultipleViews schema wrapper

    Mapping(required=[views])

    Attributes
    ----------

    views : List(anyOf(:class:`SingleView`, :class:`MultipleViews`))
        An array of view specifications
    arrangement : enum('parallel', 'serial', 'horizontal', 'vertical')
        Specify how multiple views are arranged.
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    description : string

    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    orientation : :class:`Orientation`
        Specify the orientation.
    responsiveSize : :class:`ResponsiveSize`
        Determine whether to make the size of `GoslingComponent` bound to its parent
        element. __Default__: `false`
    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    title : string

    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/RootSpecWithMultipleViews'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, views=Undefined, arrangement=Undefined, assembly=Undefined,
                 centerRadius=Undefined, description=Undefined, layout=Undefined, linkingId=Undefined,
                 orientation=Undefined, responsiveSize=Undefined, spacing=Undefined, static=Undefined,
                 style=Undefined, subtitle=Undefined, title=Undefined, xAxis=Undefined,
                 xDomain=Undefined, xOffset=Undefined, yDomain=Undefined, yOffset=Undefined,
                 zoomLimits=Undefined, **kwds):
        super(RootSpecWithMultipleViews, self).__init__(views=views, arrangement=arrangement,
                                                        assembly=assembly, centerRadius=centerRadius,
                                                        description=description, layout=layout,
                                                        linkingId=linkingId, orientation=orientation,
                                                        responsiveSize=responsiveSize, spacing=spacing,
                                                        static=static, style=style, subtitle=subtitle,
                                                        title=title, xAxis=xAxis, xDomain=xDomain,
                                                        xOffset=xOffset, yDomain=yDomain,
                                                        yOffset=yOffset, zoomLimits=zoomLimits, **kwds)


class RootSpecWithSingleView(GoslingSpec):
    """RootSpecWithSingleView schema wrapper

    anyOf(Mapping(required=[alignment, height, tracks, width]), Mapping(required=[tracks]),
    Mapping(required=[tracks]))
    """
    _schema = {'$ref': '#/definitions/RootSpecWithSingleView'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(RootSpecWithSingleView, self).__init__(*args, **kwds)


class Row(ChannelDeep):
    """Row schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    padding : float
        Determines the size of inner white spaces on the top and bottom of individiual rows.
        __Default__: `0`
    range : :class:`ValueExtent`
        Determine the start and end position of rendering area of this track along vertical
        axis. __Default__: `[0, height]`
    type : string
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/Row'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, grid=Undefined, legend=Undefined,
                 padding=Undefined, range=Undefined, type=Undefined, **kwds):
        super(Row, self).__init__(domain=domain, field=field, grid=grid, legend=legend, padding=padding,
                                  range=range, type=type, **kwds)


class SingleView(GoslingSchema):
    """SingleView schema wrapper

    anyOf(:class:`OverlaidTracks`, :class:`StackedTracks`, :class:`FlatTracks`)
    """
    _schema = {'$ref': '#/definitions/SingleView'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(SingleView, self).__init__(*args, **kwds)


class FlatTracks(SingleView):
    """FlatTracks schema wrapper

    Mapping(required=[tracks])

    Attributes
    ----------

    tracks : List(:class:`Track`)

    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    orientation : :class:`Orientation`
        Specify the orientation.
    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/FlatTracks'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, tracks=Undefined, assembly=Undefined, centerRadius=Undefined, layout=Undefined,
                 linkingId=Undefined, orientation=Undefined, spacing=Undefined, static=Undefined,
                 style=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined,
                 yDomain=Undefined, yOffset=Undefined, zoomLimits=Undefined, **kwds):
        super(FlatTracks, self).__init__(tracks=tracks, assembly=assembly, centerRadius=centerRadius,
                                         layout=layout, linkingId=linkingId, orientation=orientation,
                                         spacing=spacing, static=static, style=style, xAxis=xAxis,
                                         xDomain=xDomain, xOffset=xOffset, yDomain=yDomain,
                                         yOffset=yOffset, zoomLimits=zoomLimits, **kwds)


class OverlaidTracks(SingleView):
    """OverlaidTracks schema wrapper

    Mapping(required=[alignment, tracks, width, height])

    Attributes
    ----------

    alignment : string

    height : float
        Specify the track height in pixels.
    tracks : List(:class:`PartialTrack`)

    width : float
        Specify the track width in pixels.
    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    color : anyOf(:class:`Color`, :class:`ChannelValue`)

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    flipY : boolean

    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    mark : :class:`Mark`

    opacity : anyOf(:class:`Opacity`, :class:`ChannelValue`)

    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])
        internal
    row : anyOf(:class:`Row`, :class:`ChannelValue`)

    size : anyOf(:class:`Size`, :class:`ChannelValue`)

    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    stretch : boolean

    stroke : anyOf(:class:`Stroke`, :class:`ChannelValue`)

    strokeWidth : anyOf(:class:`StrokeWidth`, :class:`ChannelValue`)

    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    text : anyOf(:class:`Text`, :class:`ChannelValue`)

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    x : anyOf(:class:`X`, :class:`ChannelValue`)

    x1 : anyOf(:class:`X`, :class:`ChannelValue`)

    x1e : anyOf(:class:`X`, :class:`ChannelValue`)

    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    xe : anyOf(:class:`X`, :class:`ChannelValue`)

    y : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1 : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1e : anyOf(:class:`Y`, :class:`ChannelValue`)

    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    ye : anyOf(:class:`Y`, :class:`ChannelValue`)

    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/OverlaidTracks'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, alignment=Undefined, height=Undefined, tracks=Undefined, width=Undefined,
                 _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, color=Undefined, data=Undefined, dataTransform=Undefined,
                 displacement=Undefined, endAngle=Undefined, flipY=Undefined, id=Undefined,
                 innerRadius=Undefined, layout=Undefined, linkingId=Undefined, mark=Undefined,
                 opacity=Undefined, orientation=Undefined, outerRadius=Undefined,
                 overlayOnPreviousTrack=Undefined, overrideTemplate=Undefined, prerelease=Undefined,
                 row=Undefined, size=Undefined, spacing=Undefined, startAngle=Undefined,
                 static=Undefined, stretch=Undefined, stroke=Undefined, strokeWidth=Undefined,
                 style=Undefined, subtitle=Undefined, text=Undefined, title=Undefined,
                 tooltip=Undefined, visibility=Undefined, x=Undefined, x1=Undefined, x1e=Undefined,
                 xAxis=Undefined, xDomain=Undefined, xOffset=Undefined, xe=Undefined, y=Undefined,
                 y1=Undefined, y1e=Undefined, yDomain=Undefined, yOffset=Undefined, ye=Undefined,
                 zoomLimits=Undefined, **kwds):
        super(OverlaidTracks, self).__init__(alignment=alignment, height=height, tracks=tracks,
                                             width=width, _invalidTrack=_invalidTrack,
                                             _renderingId=_renderingId, assembly=assembly,
                                             centerRadius=centerRadius, color=color, data=data,
                                             dataTransform=dataTransform, displacement=displacement,
                                             endAngle=endAngle, flipY=flipY, id=id,
                                             innerRadius=innerRadius, layout=layout,
                                             linkingId=linkingId, mark=mark, opacity=opacity,
                                             orientation=orientation, outerRadius=outerRadius,
                                             overlayOnPreviousTrack=overlayOnPreviousTrack,
                                             overrideTemplate=overrideTemplate, prerelease=prerelease,
                                             row=row, size=size, spacing=spacing, startAngle=startAngle,
                                             static=static, stretch=stretch, stroke=stroke,
                                             strokeWidth=strokeWidth, style=style, subtitle=subtitle,
                                             text=text, title=title, tooltip=tooltip,
                                             visibility=visibility, x=x, x1=x1, x1e=x1e, xAxis=xAxis,
                                             xDomain=xDomain, xOffset=xOffset, xe=xe, y=y, y1=y1,
                                             y1e=y1e, yDomain=yDomain, yOffset=yOffset, ye=ye,
                                             zoomLimits=zoomLimits, **kwds)


class Size(ChannelDeep):
    """Size schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    legend : boolean
        not supported: Whether to display legend. __Default__: `false`
    range : :class:`ValueExtent`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/Size'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, legend=Undefined, range=Undefined,
                 type=Undefined, **kwds):
        super(Size, self).__init__(domain=domain, field=field, legend=legend, range=range, type=type,
                                   **kwds)


class StackedTracks(SingleView):
    """StackedTracks schema wrapper

    Mapping(required=[tracks])

    Attributes
    ----------

    tracks : List(anyOf(:class:`PartialTrack`, :class:`OverlaidTracks`))

    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    alignment : string

    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    color : anyOf(:class:`Color`, :class:`ChannelValue`)

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    flipY : boolean

    height : float
        Specify the track height in pixels.
    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    mark : :class:`Mark`

    opacity : anyOf(:class:`Opacity`, :class:`ChannelValue`)

    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])
        internal
    row : anyOf(:class:`Row`, :class:`ChannelValue`)

    size : anyOf(:class:`Size`, :class:`ChannelValue`)

    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    stretch : boolean

    stroke : anyOf(:class:`Stroke`, :class:`ChannelValue`)

    strokeWidth : anyOf(:class:`StrokeWidth`, :class:`ChannelValue`)

    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    text : anyOf(:class:`Text`, :class:`ChannelValue`)

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    width : float
        Specify the track width in pixels.
    x : anyOf(:class:`X`, :class:`ChannelValue`)

    x1 : anyOf(:class:`X`, :class:`ChannelValue`)

    x1e : anyOf(:class:`X`, :class:`ChannelValue`)

    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    xe : anyOf(:class:`X`, :class:`ChannelValue`)

    y : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1 : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1e : anyOf(:class:`Y`, :class:`ChannelValue`)

    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    ye : anyOf(:class:`Y`, :class:`ChannelValue`)

    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/StackedTracks'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, tracks=Undefined, _invalidTrack=Undefined, _renderingId=Undefined,
                 alignment=Undefined, assembly=Undefined, centerRadius=Undefined, color=Undefined,
                 data=Undefined, dataTransform=Undefined, displacement=Undefined, endAngle=Undefined,
                 flipY=Undefined, height=Undefined, id=Undefined, innerRadius=Undefined,
                 layout=Undefined, linkingId=Undefined, mark=Undefined, opacity=Undefined,
                 orientation=Undefined, outerRadius=Undefined, overlayOnPreviousTrack=Undefined,
                 overrideTemplate=Undefined, prerelease=Undefined, row=Undefined, size=Undefined,
                 spacing=Undefined, startAngle=Undefined, static=Undefined, stretch=Undefined,
                 stroke=Undefined, strokeWidth=Undefined, style=Undefined, subtitle=Undefined,
                 text=Undefined, title=Undefined, tooltip=Undefined, visibility=Undefined,
                 width=Undefined, x=Undefined, x1=Undefined, x1e=Undefined, xAxis=Undefined,
                 xDomain=Undefined, xOffset=Undefined, xe=Undefined, y=Undefined, y1=Undefined,
                 y1e=Undefined, yDomain=Undefined, yOffset=Undefined, ye=Undefined,
                 zoomLimits=Undefined, **kwds):
        super(StackedTracks, self).__init__(tracks=tracks, _invalidTrack=_invalidTrack,
                                            _renderingId=_renderingId, alignment=alignment,
                                            assembly=assembly, centerRadius=centerRadius, color=color,
                                            data=data, dataTransform=dataTransform,
                                            displacement=displacement, endAngle=endAngle, flipY=flipY,
                                            height=height, id=id, innerRadius=innerRadius,
                                            layout=layout, linkingId=linkingId, mark=mark,
                                            opacity=opacity, orientation=orientation,
                                            outerRadius=outerRadius,
                                            overlayOnPreviousTrack=overlayOnPreviousTrack,
                                            overrideTemplate=overrideTemplate, prerelease=prerelease,
                                            row=row, size=size, spacing=spacing, startAngle=startAngle,
                                            static=static, stretch=stretch, stroke=stroke,
                                            strokeWidth=strokeWidth, style=style, subtitle=subtitle,
                                            text=text, title=title, tooltip=tooltip,
                                            visibility=visibility, width=width, x=x, x1=x1, x1e=x1e,
                                            xAxis=xAxis, xDomain=xDomain, xOffset=xOffset, xe=xe, y=y,
                                            y1=y1, y1e=y1e, yDomain=yDomain, yOffset=yOffset, ye=ye,
                                            zoomLimits=zoomLimits, **kwds)


class StrConcatTransform(DataTransform):
    """StrConcatTransform schema wrapper

    Mapping(required=[type, fields, newField, separator])

    Attributes
    ----------

    fields : List(string)

    newField : string

    separator : string

    type : string

    """
    _schema = {'$ref': '#/definitions/StrConcatTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, fields=Undefined, newField=Undefined, separator=Undefined, type=Undefined, **kwds):
        super(StrConcatTransform, self).__init__(fields=fields, newField=newField, separator=separator,
                                                 type=type, **kwds)


class StrReplaceTransform(DataTransform):
    """StrReplaceTransform schema wrapper

    Mapping(required=[type, field, newField, replace])

    Attributes
    ----------

    field : string

    newField : string

    replace : List(Mapping(required=[from, to]))

    type : string

    """
    _schema = {'$ref': '#/definitions/StrReplaceTransform'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, newField=Undefined, replace=Undefined, type=Undefined, **kwds):
        super(StrReplaceTransform, self).__init__(field=field, newField=newField, replace=replace,
                                                  type=type, **kwds)


class Stroke(ChannelDeep):
    """Stroke schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    range : :class:`Range`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/Stroke'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, range=Undefined, type=Undefined, **kwds):
        super(Stroke, self).__init__(domain=domain, field=field, range=range, type=type, **kwds)


class StrokeWidth(ChannelDeep):
    """StrokeWidth schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    range : :class:`ValueExtent`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/StrokeWidth'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, range=Undefined, type=Undefined, **kwds):
        super(StrokeWidth, self).__init__(domain=domain, field=field, range=range, type=type, **kwds)


class Style(GoslingSchema):
    """Style schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    align : enum('left', 'right')
        Specify the alignment of marks. This property is currently only supported for
        `triangle` marks.
    background : string

    backgroundOpacity : float

    bezierLink : boolean
        Specify whether to use bezier curves for the `link` marks.
    curve : enum('top', 'bottom', 'left', 'right')
        Specify the curve of `rule` marks.
    dashed : List([float, float])
        Specify the pattern of dashes and gaps for `rule` marks.
    dx : float
        Offset the position of marks in x direction. This property is currently only
        supported for `text` marks
    dy : float
        Offset the position of marks in y direction. This property is currently only
        supported for `text` marks.
    enableSmoothPath : boolean
        Whether to enable smooth paths when drawing curves.

        __Default__: `false`
    flatWithinLink : boolean
        Specify whether to use a flat within-links, such as the one in Sashimi plots.
        __Default__: `false`
    inlineLegend : boolean
        Specify whether to show legend in a single horizontal line?
    legendTitle : string
        If defined, show legend title on the top or left
    linePattern : Mapping(required=[type, size])
        Specify the pattern of dashes and gaps for `rule` marks.
    linkConnectionType : enum('straight', 'curve', 'corner')
        Specify the connetion type of `betweenLink` marks.

        __Default__: `"corner"`
    outline : string

    outlineWidth : float

    textAnchor : enum('start', 'middle', 'end')
        Specify the alignment of `text` marks to a given point.
    textFontSize : float
        Specify the font size of `text` marks. Can also be specified using the `size`
        channel option of `text` marks.
    textFontWeight : enum('bold', 'normal')
        Specify the font weight of `text` marks.
    textStroke : string
        Specify the stroke of `text` marks. Can also be specified using the `stroke` channel
        option of `text` marks.
    textStrokeWidth : float
        Specify the stroke width of `text` marks. Can also be specified using the
        `strokeWidth` channel option of `text` marks.
    """
    _schema = {'$ref': '#/definitions/Style'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                 bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                 enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                 legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                 outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                 textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                 textStrokeWidth=Undefined, **kwds):
        super(Style, self).__init__(align=align, background=background,
                                    backgroundOpacity=backgroundOpacity, bezierLink=bezierLink,
                                    curve=curve, dashed=dashed, dx=dx, dy=dy,
                                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                                    inlineLegend=inlineLegend, legendTitle=legendTitle,
                                    linePattern=linePattern, linkConnectionType=linkConnectionType,
                                    outline=outline, outlineWidth=outlineWidth, textAnchor=textAnchor,
                                    textFontSize=textFontSize, textFontWeight=textFontWeight,
                                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)


class Text(ChannelDeep):
    """Text schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    domain : List(string)
        Values of the data
    field : string
        Name of the data field
    range : List(string)
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _schema = {'$ref': '#/definitions/Text'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, domain=Undefined, field=Undefined, range=Undefined, type=Undefined, **kwds):
        super(Text, self).__init__(domain=domain, field=field, range=range, type=type, **kwds)


class Tooltip(GoslingSchema):
    """Tooltip schema wrapper

    Mapping(required=[field, type])

    Attributes
    ----------

    field : string

    type : :class:`FieldType`

    alt : string

    format : string

    """
    _schema = {'$ref': '#/definitions/Tooltip'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, type=Undefined, alt=Undefined, format=Undefined, **kwds):
        super(Tooltip, self).__init__(field=field, type=type, alt=alt, format=format, **kwds)


class Track(GoslingSchema):
    """Track schema wrapper

    anyOf(:class:`SingleTrack`, :class:`OverlaidTrack`, :class:`DataTrack`,
    :class:`TemplateTrack`)
    """
    _schema = {'$ref': '#/definitions/Track'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Track, self).__init__(*args, **kwds)


class DataTrack(Track):
    """DataTrack schema wrapper

    Mapping(required=[data, height, width])
    Partial specification of `BasicSingleTrack` to use default visual encoding predefined by
    data type.

    Attributes
    ----------

    data : :class:`DataDeep`

    height : float
        Specify the track height in pixels.
    width : float
        Specify the track width in pixels.
    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlayOnPreviousTrack : boolean

    prerelease : Mapping(required=[])
        internal
    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/DataTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, data=Undefined, height=Undefined, width=Undefined, _invalidTrack=Undefined,
                 _renderingId=Undefined, assembly=Undefined, centerRadius=Undefined, endAngle=Undefined,
                 id=Undefined, innerRadius=Undefined, layout=Undefined, linkingId=Undefined,
                 orientation=Undefined, outerRadius=Undefined, overlayOnPreviousTrack=Undefined,
                 prerelease=Undefined, spacing=Undefined, startAngle=Undefined, static=Undefined,
                 style=Undefined, subtitle=Undefined, title=Undefined, xAxis=Undefined,
                 xDomain=Undefined, xOffset=Undefined, yDomain=Undefined, yOffset=Undefined,
                 zoomLimits=Undefined, **kwds):
        super(DataTrack, self).__init__(data=data, height=height, width=width,
                                        _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                        assembly=assembly, centerRadius=centerRadius, endAngle=endAngle,
                                        id=id, innerRadius=innerRadius, layout=layout,
                                        linkingId=linkingId, orientation=orientation,
                                        outerRadius=outerRadius,
                                        overlayOnPreviousTrack=overlayOnPreviousTrack,
                                        prerelease=prerelease, spacing=spacing, startAngle=startAngle,
                                        static=static, style=style, subtitle=subtitle, title=title,
                                        xAxis=xAxis, xDomain=xDomain, xOffset=xOffset, yDomain=yDomain,
                                        yOffset=yOffset, zoomLimits=zoomLimits, **kwds)


class OverlaidTrack(Track):
    """OverlaidTrack schema wrapper

    Mapping(required=[height, overlay, width])
    Superposing multiple tracks.

    Attributes
    ----------

    height : float
        Specify the track height in pixels.
    overlay : List(Mapping(required=[]))

    width : float
        Specify the track width in pixels.
    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    color : anyOf(:class:`Color`, :class:`ChannelValue`)

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    flipY : boolean

    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    mark : :class:`Mark`

    opacity : anyOf(:class:`Opacity`, :class:`ChannelValue`)

    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])
        internal
    row : anyOf(:class:`Row`, :class:`ChannelValue`)

    size : anyOf(:class:`Size`, :class:`ChannelValue`)

    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    stretch : boolean

    stroke : anyOf(:class:`Stroke`, :class:`ChannelValue`)

    strokeWidth : anyOf(:class:`StrokeWidth`, :class:`ChannelValue`)

    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    text : anyOf(:class:`Text`, :class:`ChannelValue`)

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    x : anyOf(:class:`X`, :class:`ChannelValue`)

    x1 : anyOf(:class:`X`, :class:`ChannelValue`)

    x1e : anyOf(:class:`X`, :class:`ChannelValue`)

    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    xe : anyOf(:class:`X`, :class:`ChannelValue`)

    y : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1 : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1e : anyOf(:class:`Y`, :class:`ChannelValue`)

    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    ye : anyOf(:class:`Y`, :class:`ChannelValue`)

    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/OverlaidTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, height=Undefined, overlay=Undefined, width=Undefined, _invalidTrack=Undefined,
                 _renderingId=Undefined, assembly=Undefined, centerRadius=Undefined, color=Undefined,
                 data=Undefined, dataTransform=Undefined, displacement=Undefined, endAngle=Undefined,
                 flipY=Undefined, id=Undefined, innerRadius=Undefined, layout=Undefined,
                 linkingId=Undefined, mark=Undefined, opacity=Undefined, orientation=Undefined,
                 outerRadius=Undefined, overlayOnPreviousTrack=Undefined, overrideTemplate=Undefined,
                 prerelease=Undefined, row=Undefined, size=Undefined, spacing=Undefined,
                 startAngle=Undefined, static=Undefined, stretch=Undefined, stroke=Undefined,
                 strokeWidth=Undefined, style=Undefined, subtitle=Undefined, text=Undefined,
                 title=Undefined, tooltip=Undefined, visibility=Undefined, x=Undefined, x1=Undefined,
                 x1e=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined, xe=Undefined,
                 y=Undefined, y1=Undefined, y1e=Undefined, yDomain=Undefined, yOffset=Undefined,
                 ye=Undefined, zoomLimits=Undefined, **kwds):
        super(OverlaidTrack, self).__init__(height=height, overlay=overlay, width=width,
                                            _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                            assembly=assembly, centerRadius=centerRadius, color=color,
                                            data=data, dataTransform=dataTransform,
                                            displacement=displacement, endAngle=endAngle, flipY=flipY,
                                            id=id, innerRadius=innerRadius, layout=layout,
                                            linkingId=linkingId, mark=mark, opacity=opacity,
                                            orientation=orientation, outerRadius=outerRadius,
                                            overlayOnPreviousTrack=overlayOnPreviousTrack,
                                            overrideTemplate=overrideTemplate, prerelease=prerelease,
                                            row=row, size=size, spacing=spacing, startAngle=startAngle,
                                            static=static, stretch=stretch, stroke=stroke,
                                            strokeWidth=strokeWidth, style=style, subtitle=subtitle,
                                            text=text, title=title, tooltip=tooltip,
                                            visibility=visibility, x=x, x1=x1, x1e=x1e, xAxis=xAxis,
                                            xDomain=xDomain, xOffset=xOffset, xe=xe, y=y, y1=y1,
                                            y1e=y1e, yDomain=yDomain, yOffset=yOffset, ye=ye,
                                            zoomLimits=zoomLimits, **kwds)


class SingleTrack(Track):
    """SingleTrack schema wrapper

    Mapping(required=[data, height, mark, width])

    Attributes
    ----------

    data : :class:`DataDeep`

    height : float
        Specify the track height in pixels.
    mark : :class:`Mark`

    width : float
        Specify the track width in pixels.
    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    color : anyOf(:class:`Color`, :class:`ChannelValue`)

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    flipY : boolean

    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    opacity : anyOf(:class:`Opacity`, :class:`ChannelValue`)

    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])
        internal
    row : anyOf(:class:`Row`, :class:`ChannelValue`)

    size : anyOf(:class:`Size`, :class:`ChannelValue`)

    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    stretch : boolean

    stroke : anyOf(:class:`Stroke`, :class:`ChannelValue`)

    strokeWidth : anyOf(:class:`StrokeWidth`, :class:`ChannelValue`)

    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    text : anyOf(:class:`Text`, :class:`ChannelValue`)

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    x : anyOf(:class:`X`, :class:`ChannelValue`)

    x1 : anyOf(:class:`X`, :class:`ChannelValue`)

    x1e : anyOf(:class:`X`, :class:`ChannelValue`)

    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    xe : anyOf(:class:`X`, :class:`ChannelValue`)

    y : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1 : anyOf(:class:`Y`, :class:`ChannelValue`)

    y1e : anyOf(:class:`Y`, :class:`ChannelValue`)

    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    ye : anyOf(:class:`Y`, :class:`ChannelValue`)

    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/SingleTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, data=Undefined, height=Undefined, mark=Undefined, width=Undefined,
                 _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, color=Undefined, dataTransform=Undefined,
                 displacement=Undefined, endAngle=Undefined, flipY=Undefined, id=Undefined,
                 innerRadius=Undefined, layout=Undefined, linkingId=Undefined, opacity=Undefined,
                 orientation=Undefined, outerRadius=Undefined, overlayOnPreviousTrack=Undefined,
                 overrideTemplate=Undefined, prerelease=Undefined, row=Undefined, size=Undefined,
                 spacing=Undefined, startAngle=Undefined, static=Undefined, stretch=Undefined,
                 stroke=Undefined, strokeWidth=Undefined, style=Undefined, subtitle=Undefined,
                 text=Undefined, title=Undefined, tooltip=Undefined, visibility=Undefined, x=Undefined,
                 x1=Undefined, x1e=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined,
                 xe=Undefined, y=Undefined, y1=Undefined, y1e=Undefined, yDomain=Undefined,
                 yOffset=Undefined, ye=Undefined, zoomLimits=Undefined, **kwds):
        super(SingleTrack, self).__init__(data=data, height=height, mark=mark, width=width,
                                          _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                          assembly=assembly, centerRadius=centerRadius, color=color,
                                          dataTransform=dataTransform, displacement=displacement,
                                          endAngle=endAngle, flipY=flipY, id=id,
                                          innerRadius=innerRadius, layout=layout, linkingId=linkingId,
                                          opacity=opacity, orientation=orientation,
                                          outerRadius=outerRadius,
                                          overlayOnPreviousTrack=overlayOnPreviousTrack,
                                          overrideTemplate=overrideTemplate, prerelease=prerelease,
                                          row=row, size=size, spacing=spacing, startAngle=startAngle,
                                          static=static, stretch=stretch, stroke=stroke,
                                          strokeWidth=strokeWidth, style=style, subtitle=subtitle,
                                          text=text, title=title, tooltip=tooltip,
                                          visibility=visibility, x=x, x1=x1, x1e=x1e, xAxis=xAxis,
                                          xDomain=xDomain, xOffset=xOffset, xe=xe, y=y, y1=y1, y1e=y1e,
                                          yDomain=yDomain, yOffset=yOffset, ye=ye,
                                          zoomLimits=zoomLimits, **kwds)


class TemplateTrack(Track):
    """TemplateTrack schema wrapper

    Mapping(required=[data, height, template, width])
    Template specification that will be internally converted into `SingleTrack` for rendering.

    Attributes
    ----------

    data : :class:`DataDeep`

    height : float
        Specify the track height in pixels.
    template : string

    width : float
        Specify the track width in pixels.
    _invalidTrack : boolean
        internal
    _renderingId : string
        internal
    assembly : :class:`Assembly`
        A string that specifies the genome builds to use. Currently support `"hg38"`,
        `"hg19"`, `"hg18"`, `"hg17"`, `"hg16"`, `"mm10"`, `"mm9"`, and `"unknown"`.

        __Note:__: with `"unknown"` assembly, genomic axes do not show chrN: in labels.
    centerRadius : float
        Proportion of the radius of the center white space.

        __Default:__ `0.3`
    encoding : Mapping(required=[])

    endAngle : float
        Specify the end angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    id : string

    innerRadius : float
        Specify the inner radius of tracks when (`{"layout": "circular"}`).
    layout : :class:`Layout`
        Specify the layout type of all tracks.
    linkingId : string
        Specify an ID for [linking multiple
        views](http://gosling-lang.org/docs/user-interaction#linking-views)
    orientation : :class:`Orientation`
        Specify the orientation.
    outerRadius : float
        Specify the outer radius of tracks when `{"layout": "circular"}`.
    overlayOnPreviousTrack : boolean

    prerelease : Mapping(required=[])
        internal
    spacing : float
        - If `{"layout": "linear"}`, specify the space between tracks in pixels;

        - If `{"layout": "circular"}`, specify the space between tracks in percentage
        ranging from 0 to 100.
    startAngle : float
        Specify the start angle (in the range of [0, 360]) of circular tracks (`{"layout":
        "circular"}`).
    static : boolean
        Whether to disable [Zooming and
        Panning](http://gosling-lang.org/docs/user-interaction#zooming-and-panning),
        __Default:__ `false`.
    style : :class:`Style`
        Define the
        [style](http://gosling-lang.org/docs/visual-channel#style-related-properties) of
        multive views. Will be overriden by the style of children elements (e.g., view,
        track).
    subtitle : string

    title : string
        If defined, will show the textual label on the left-top corner of a track.
    xAxis : :class:`AxisPosition`
        not supported
    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic x-axis
    xOffset : float
        Specify the x offset of views in the unit of pixels
    yDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)
        Specify the visible region of genomic y-axis
    yOffset : float
        Specify the y offset of views in the unit of pixels
    zoomLimits : :class:`ZoomLimits`

    """
    _schema = {'$ref': '#/definitions/TemplateTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, data=Undefined, height=Undefined, template=Undefined, width=Undefined,
                 _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, encoding=Undefined, endAngle=Undefined, id=Undefined,
                 innerRadius=Undefined, layout=Undefined, linkingId=Undefined, orientation=Undefined,
                 outerRadius=Undefined, overlayOnPreviousTrack=Undefined, prerelease=Undefined,
                 spacing=Undefined, startAngle=Undefined, static=Undefined, style=Undefined,
                 subtitle=Undefined, title=Undefined, xAxis=Undefined, xDomain=Undefined,
                 xOffset=Undefined, yDomain=Undefined, yOffset=Undefined, zoomLimits=Undefined, **kwds):
        super(TemplateTrack, self).__init__(data=data, height=height, template=template, width=width,
                                            _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                            assembly=assembly, centerRadius=centerRadius,
                                            encoding=encoding, endAngle=endAngle, id=id,
                                            innerRadius=innerRadius, layout=layout, linkingId=linkingId,
                                            orientation=orientation, outerRadius=outerRadius,
                                            overlayOnPreviousTrack=overlayOnPreviousTrack,
                                            prerelease=prerelease, spacing=spacing,
                                            startAngle=startAngle, static=static, style=style,
                                            subtitle=subtitle, title=title, xAxis=xAxis,
                                            xDomain=xDomain, xOffset=xOffset, yDomain=yDomain,
                                            yOffset=yOffset, zoomLimits=zoomLimits, **kwds)


class ValueExtent(Range):
    """ValueExtent schema wrapper

    anyOf(List(string), List(float))
    """
    _schema = {'$ref': '#/definitions/ValueExtent'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(ValueExtent, self).__init__(*args, **kwds)


class VectorData(DataDeep):
    """VectorData schema wrapper

    Mapping(required=[type, url, column, value])
    One-dimensional quantitative values along genomic position (e.g., bigwig) can be converted
    into HiGlass' `"vector"` format data. Find out more about this format at [HiGlass
    Docs](https://docs.higlass.io/data_preparation.html#bigwig-files).

    Attributes
    ----------

    column : string
        Assign a field name of the middle position of genomic intervals.
    type : string

    url : string
        Specify the URL address of the data file.
    value : string
        Assign a field name of quantitative values.
    aggregation : :class:`BinAggregate`
        Determine aggregation function to apply within bins. __Default__: `"mean"`
    binSize : float
        Binning the genomic interval in tiles (unit size: 256).
    end : string
        Assign a field name of the end position of genomic intervals.
    start : string
        Assign a field name of the start position of genomic intervals.
    """
    _schema = {'$ref': '#/definitions/VectorData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, column=Undefined, type=Undefined, url=Undefined, value=Undefined,
                 aggregation=Undefined, binSize=Undefined, end=Undefined, start=Undefined, **kwds):
        super(VectorData, self).__init__(column=column, type=type, url=url, value=value,
                                         aggregation=aggregation, binSize=binSize, end=end, start=start,
                                         **kwds)


class VisibilityCondition(GoslingSchema):
    """VisibilityCondition schema wrapper

    anyOf(:class:`SizeVisibilityCondition`, :class:`ZoomLevelVisibilityCondition`)
    """
    _schema = {'$ref': '#/definitions/VisibilityCondition'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(VisibilityCondition, self).__init__(*args, **kwds)


class SizeVisibilityCondition(VisibilityCondition):
    """SizeVisibilityCondition schema wrapper

    Mapping(required=[measure, operation, target, threshold])

    Attributes
    ----------

    measure : enum('width', 'height')
        Specify which aspect of the `target` will be compared to the `threshold`.
    operation : :class:`LogicalOperation`
        A string that pecifies the logical operation to conduct between `threshold` and the
        `measure` of `target`. Support

        - greater than : "greater-than", "gt", "GT"

        - less than : "less-than", "lt", "LT"

        - greater than or equal to : "greater-than-or-equal-to", "gtet", "GTET"

        - less than or equal to : "less-than-or-equal-to", "ltet", "LTET"
    target : enum('track', 'mark')
        Target specifies the object that you want to compare with the threshold.
    threshold : anyOf(float, string)
        Specify the threshold as one of:

        - A number representing a fixed threshold in the unit of pixels;

        - `"|xe-x|"`, using the distance between `xe` and `x` as threshold
    conditionPadding : float
        Specify the buffer size (in pixel) of width or height when calculating the
        visibility.

        __Default__: `0`
    transitionPadding : float
        Specify the buffer size (in pixel) of width or height for smooth transition.

        __Default__: `0`
    """
    _schema = {'$ref': '#/definitions/SizeVisibilityCondition'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, measure=Undefined, operation=Undefined, target=Undefined, threshold=Undefined,
                 conditionPadding=Undefined, transitionPadding=Undefined, **kwds):
        super(SizeVisibilityCondition, self).__init__(measure=measure, operation=operation,
                                                      target=target, threshold=threshold,
                                                      conditionPadding=conditionPadding,
                                                      transitionPadding=transitionPadding, **kwds)


class X(ChannelDeep):
    """X schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    domain : :class:`GenomicDomain`
        Values of the data
    field : string
        Name of the data field.
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : string
        Specify the data type.
    """
    _schema = {'$ref': '#/definitions/X'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, aggregate=Undefined, axis=Undefined, domain=Undefined, field=Undefined,
                 grid=Undefined, legend=Undefined, linkingId=Undefined, range=Undefined, type=Undefined,
                 **kwds):
        super(X, self).__init__(aggregate=aggregate, axis=axis, domain=domain, field=field, grid=grid,
                                legend=legend, linkingId=linkingId, range=range, type=type, **kwds)


class Y(ChannelDeep):
    """Y schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    baseline : anyOf(string, float)
        Custom baseline of the y-axis. __Default__: `0`
    domain : anyOf(:class:`ValueExtent`, :class:`GenomicDomain`)
        Values of the data
    field : string
        Name of the data field.
    flip : boolean
        Whether to flip the y-axis. This is done by inverting the `range` property.
        __Default__: `false`
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : enum('quantitative', 'nominal', 'genomic')
        Specify the data type.
    zeroBaseline : boolean
        Specify whether to use zero baseline. __Default__: `true`
    """
    _schema = {'$ref': '#/definitions/Y'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, aggregate=Undefined, axis=Undefined, baseline=Undefined, domain=Undefined,
                 field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined, linkingId=Undefined,
                 range=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(Y, self).__init__(aggregate=aggregate, axis=axis, baseline=baseline, domain=domain,
                                field=field, flip=flip, grid=grid, legend=legend, linkingId=linkingId,
                                range=range, type=type, zeroBaseline=zeroBaseline, **kwds)


class ZoomLevelVisibilityCondition(VisibilityCondition):
    """ZoomLevelVisibilityCondition schema wrapper

    Mapping(required=[measure, operation, target, threshold])

    Attributes
    ----------

    measure : string
        Specify which aspect of the `target` will be compared to the `threshold`.
    operation : :class:`LogicalOperation`
        A string that pecifies the logical operation to conduct between `threshold` and the
        `measure` of `target`. Support

        - greater than : "greater-than", "gt", "GT"

        - less than : "less-than", "lt", "LT"

        - greater than or equal to : "greater-than-or-equal-to", "gtet", "GTET"

        - less than or equal to : "less-than-or-equal-to", "ltet", "LTET"
    target : enum('track', 'mark')
        Target specifies the object that you want to compare with the threshold.
    threshold : float
        Set a threshold in the unit of base pairs (bp)
    conditionPadding : float
        Specify the buffer size (in pixel) of width or height when calculating the
        visibility.

        __Default__: `0`
    transitionPadding : float
        Specify the buffer size (in pixel) of width or height for smooth transition.

        __Default__: `0`
    """
    _schema = {'$ref': '#/definitions/ZoomLevelVisibilityCondition'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, measure=Undefined, operation=Undefined, target=Undefined, threshold=Undefined,
                 conditionPadding=Undefined, transitionPadding=Undefined, **kwds):
        super(ZoomLevelVisibilityCondition, self).__init__(measure=measure, operation=operation,
                                                           target=target, threshold=threshold,
                                                           conditionPadding=conditionPadding,
                                                           transitionPadding=transitionPadding, **kwds)


class ZoomLimits(GoslingSchema):
    """ZoomLimits schema wrapper

    List([anyOf(float, None), anyOf(float, None)])
    """
    _schema = {'$ref': '#/definitions/ZoomLimits'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(ZoomLimits, self).__init__(*args)

