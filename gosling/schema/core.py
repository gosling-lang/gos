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


class Channel(GoslingSchema):
    """Channel schema wrapper

    anyOf(:class:`ChannelDeep`, :class:`ChannelValue`)
    """
    _schema = {'$ref': '#/definitions/Channel'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Channel, self).__init__(*args, **kwds)


class ChannelBind(GoslingSchema):
    """ChannelBind schema wrapper

    Mapping(required=[bind])

    Attributes
    ----------

    bind : :class:`ChannelType`

    aggregate : :class:`Aggregate`

    """
    _schema = {'$ref': '#/definitions/ChannelBind'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, bind=Undefined, aggregate=Undefined, **kwds):
        super(ChannelBind, self).__init__(bind=bind, aggregate=aggregate, **kwds)


class ChannelDeep(Channel):
    """ChannelDeep schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    aggregate : :class:`Aggregate`

    axis : :class:`AxisPosition`

    baseline : anyOf(string, float)

    domain : :class:`Domain`

    field : string

    flip : boolean

    grid : boolean

    legend : boolean

    linkingId : string

    mirrored : boolean

    padding : float

    range : :class:`Range`

    sort : List(string)

    stack : boolean

    type : :class:`FieldType`

    zeroBaseline : boolean

    """
    _schema = {'$ref': '#/definitions/ChannelDeep'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, aggregate=Undefined, axis=Undefined, baseline=Undefined, domain=Undefined,
                 field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined, linkingId=Undefined,
                 mirrored=Undefined, padding=Undefined, range=Undefined, sort=Undefined,
                 stack=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(ChannelDeep, self).__init__(aggregate=aggregate, axis=axis, baseline=baseline,
                                          domain=domain, field=field, flip=flip, grid=grid,
                                          legend=legend, linkingId=linkingId, mirrored=mirrored,
                                          padding=padding, range=range, sort=sort, stack=stack,
                                          type=type, zeroBaseline=zeroBaseline, **kwds)


class ChannelType(GoslingSchema):
    """ChannelType schema wrapper

    string
    """
    _schema = {'$ref': '#/definitions/ChannelType'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(ChannelType, self).__init__(*args)


class ChannelValue(Channel):
    """ChannelValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)

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

    Attributes
    ----------

    indexUrl : string

    type : string

    url : string

    """
    _schema = {'$ref': '#/definitions/BAMData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, indexUrl=Undefined, type=Undefined, url=Undefined, **kwds):
        super(BAMData, self).__init__(indexUrl=indexUrl, type=type, url=url, **kwds)


class BEDDBData(DataDeep):
    """BEDDBData schema wrapper

    Mapping(required=[type, url, genomicFields])

    Attributes
    ----------

    genomicFields : List(Mapping(required=[index, name]))

    type : string

    url : string

    exonIntervalFields : List([Mapping(required=[index, name]), Mapping(required=[index,
    name])])

    valueFields : List(Mapping(required=[index, name, type]))

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

    type : string

    url : string

    value : string

    binSize : float

    end : string

    start : string

    """
    _schema = {'$ref': '#/definitions/BIGWIGData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, column=Undefined, type=Undefined, url=Undefined, value=Undefined,
                 binSize=Undefined, end=Undefined, start=Undefined, **kwds):
        super(BIGWIGData, self).__init__(column=column, type=type, url=url, value=value,
                                         binSize=binSize, end=end, start=start, **kwds)


class CSVData(DataDeep):
    """CSVData schema wrapper

    Mapping(required=[type, url])

    Attributes
    ----------

    type : string

    url : string

    chromosomeField : string

    chromosomePrefix : string

    genomicFields : List(string)

    genomicFieldsToConvert : List(Mapping(required=[chromosomeField, genomicFields]))

    headerNames : List(string)

    longToWideId : string

    quantitativeFields : List(string)

    sampleLength : float

    separator : string

    """
    _schema = {'$ref': '#/definitions/CSVData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, url=Undefined, chromosomeField=Undefined,
                 chromosomePrefix=Undefined, genomicFields=Undefined, genomicFieldsToConvert=Undefined,
                 headerNames=Undefined, longToWideId=Undefined, quantitativeFields=Undefined,
                 sampleLength=Undefined, separator=Undefined, **kwds):
        super(CSVData, self).__init__(type=type, url=url, chromosomeField=chromosomeField,
                                      chromosomePrefix=chromosomePrefix, genomicFields=genomicFields,
                                      genomicFieldsToConvert=genomicFieldsToConvert,
                                      headerNames=headerNames, longToWideId=longToWideId,
                                      quantitativeFields=quantitativeFields, sampleLength=sampleLength,
                                      separator=separator, **kwds)


class DataTransform(GoslingSchema):
    """DataTransform schema wrapper

    anyOf(:class:`FilterTransform`, :class:`StrConcatTransform`, :class:`StrReplaceTransform`,
    :class:`LogTransform`, :class:`DisplaceTransform`, :class:`ExonSplitTransform`,
    :class:`CoverageTransform`, :class:`JSONParseTransform`)
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

    newField : string

    type : string

    maxRows : float

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


class Domain(GoslingSchema):
    """Domain schema wrapper

    anyOf(List(string), List(float), :class:`DomainInterval`, :class:`DomainChrInterval`,
    :class:`DomainChr`, :class:`DomainGene`)
    """
    _schema = {'$ref': '#/definitions/Domain'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Domain, self).__init__(*args, **kwds)


class DomainChr(Domain):
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


class DomainChrInterval(Domain):
    """DomainChrInterval schema wrapper

    Mapping(required=[chromosome, interval])

    Attributes
    ----------

    chromosome : :class:`Chromosome`

    interval : List([float, float])

    """
    _schema = {'$ref': '#/definitions/DomainChrInterval'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, chromosome=Undefined, interval=Undefined, **kwds):
        super(DomainChrInterval, self).__init__(chromosome=chromosome, interval=interval, **kwds)


class DomainGene(Domain):
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


class DomainInterval(Domain):
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


class GlyphElement(GoslingSchema):
    """GlyphElement schema wrapper

    Mapping(required=[mark])

    Attributes
    ----------

    mark : anyOf(:class:`MarkType`, :class:`MarkBind`)

    background : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    color : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    description : string

    opacity : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    row : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    select : List(Mapping(required=[channel, oneOf]))

    size : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    stroke : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    strokeWidth : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    style : :class:`MarkStyleInGlyph`

    text : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    w : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    x : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    x1 : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    x1e : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    xe : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    y : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    y1 : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    y1e : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    ye : anyOf(:class:`ChannelBind`, :class:`ChannelValue`, string)

    """
    _schema = {'$ref': '#/definitions/GlyphElement'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, mark=Undefined, background=Undefined, color=Undefined, description=Undefined,
                 opacity=Undefined, row=Undefined, select=Undefined, size=Undefined, stroke=Undefined,
                 strokeWidth=Undefined, style=Undefined, text=Undefined, w=Undefined, x=Undefined,
                 x1=Undefined, x1e=Undefined, xe=Undefined, y=Undefined, y1=Undefined, y1e=Undefined,
                 ye=Undefined, **kwds):
        super(GlyphElement, self).__init__(mark=mark, background=background, color=color,
                                           description=description, opacity=opacity, row=row,
                                           select=select, size=size, stroke=stroke,
                                           strokeWidth=strokeWidth, style=style, text=text, w=w, x=x,
                                           x1=x1, x1e=x1e, xe=xe, y=y, y1=y1, y1e=y1e, ye=ye, **kwds)


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

    Mapping(required=[type, field, include])

    Attributes
    ----------

    field : string

    include : string

    type : string

    not : boolean

    """
    _schema = {'$ref': '#/definitions/IncludeFilter'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, include=Undefined, type=Undefined, **kwds):
        super(IncludeFilter, self).__init__(field=field, include=include, type=type, **kwds)


class JSONData(DataDeep):
    """JSONData schema wrapper

    Mapping(required=[type, values])

    Attributes
    ----------

    type : string

    values : List(:class:`Datum`)

    chromosomeField : string

    genomicFields : List(string)

    genomicFieldsToConvert : List(Mapping(required=[chromosomeField, genomicFields]))

    quantitativeFields : List(string)

    sampleLength : float

    """
    _schema = {'$ref': '#/definitions/JSONData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, values=Undefined, chromosomeField=Undefined,
                 genomicFields=Undefined, genomicFieldsToConvert=Undefined,
                 quantitativeFields=Undefined, sampleLength=Undefined, **kwds):
        super(JSONData, self).__init__(type=type, values=values, chromosomeField=chromosomeField,
                                       genomicFields=genomicFields,
                                       genomicFieldsToConvert=genomicFieldsToConvert,
                                       quantitativeFields=quantitativeFields, sampleLength=sampleLength,
                                       **kwds)


class JSONParseTransform(DataTransform):
    """JSONParseTransform schema wrapper

    Mapping(required=[type, field, baseGenomicField, genomicField, genomicLengthField])
    Parse JSON Object Array and append vertically

    Attributes
    ----------

    baseGenomicField : string

    field : string

    genomicField : string

    genomicLengthField : string

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

    newField : string

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

    anyOf(:class:`MarkType`, :class:`MarkDeep`)
    """
    _schema = {'$ref': '#/definitions/Mark'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Mark, self).__init__(*args, **kwds)


class MarkBind(GoslingSchema):
    """MarkBind schema wrapper

    Mapping(required=[bind, domain, range])

    Attributes
    ----------

    bind : string

    domain : List(string)

    range : List(:class:`MarkType`)

    """
    _schema = {'$ref': '#/definitions/MarkBind'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, bind=Undefined, domain=Undefined, range=Undefined, **kwds):
        super(MarkBind, self).__init__(bind=bind, domain=domain, range=range, **kwds)


class MarkDeep(Mark):
    """MarkDeep schema wrapper

    anyOf(:class:`MarkGlyphPreset`, :class:`MarkGlyph`)
    """
    _schema = {'$ref': '#/definitions/MarkDeep'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(MarkDeep, self).__init__(*args, **kwds)


class MarkGlyph(MarkDeep):
    """MarkGlyph schema wrapper

    Mapping(required=[type, name, requiredChannels, elements])

    Attributes
    ----------

    elements : List(:class:`GlyphElement`)

    name : string

    requiredChannels : List(:class:`ChannelType`)

    type : string

    referenceColumn : string

    """
    _schema = {'$ref': '#/definitions/MarkGlyph'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, elements=Undefined, name=Undefined, requiredChannels=Undefined, type=Undefined,
                 referenceColumn=Undefined, **kwds):
        super(MarkGlyph, self).__init__(elements=elements, name=name, requiredChannels=requiredChannels,
                                        type=type, referenceColumn=referenceColumn, **kwds)


class MarkGlyphPreset(MarkDeep):
    """MarkGlyphPreset schema wrapper

    Mapping(required=[type, server])

    Attributes
    ----------

    server : string

    type : string

    """
    _schema = {'$ref': '#/definitions/MarkGlyphPreset'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, server=Undefined, type=Undefined, **kwds):
        super(MarkGlyphPreset, self).__init__(server=server, type=type, **kwds)


class MarkStyleInGlyph(GoslingSchema):
    """MarkStyleInGlyph schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    background : string

    dashed : string

    dy : float

    stroke : string

    strokeWidth : float

    """
    _schema = {'$ref': '#/definitions/MarkStyleInGlyph'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, background=Undefined, dashed=Undefined, dy=Undefined, stroke=Undefined,
                 strokeWidth=Undefined, **kwds):
        super(MarkStyleInGlyph, self).__init__(background=background, dashed=dashed, dy=dy,
                                               stroke=stroke, strokeWidth=strokeWidth, **kwds)


class MarkType(Mark):
    """MarkType schema wrapper

    enum('point', 'line', 'area', 'bar', 'rect', 'text', 'withinLink', 'betweenLink', 'rule',
    'triangleLeft', 'triangleRight', 'triangleBottom', 'brush', 'header')
    """
    _schema = {'$ref': '#/definitions/MarkType'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(MarkType, self).__init__(*args)


class MatrixData(DataDeep):
    """MatrixData schema wrapper

    Mapping(required=[type, url])

    Attributes
    ----------

    type : string

    url : string

    """
    _schema = {'$ref': '#/definitions/MatrixData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, type=Undefined, url=Undefined, **kwds):
        super(MatrixData, self).__init__(type=type, url=url, **kwds)


class MultipleViews(GoslingSchema):
    """MultipleViews schema wrapper

    Mapping(required=[views])

    Attributes
    ----------

    views : List(anyOf(:class:`SingleView`, :class:`MultipleViews`))

    arrangement : enum('parallel', 'serial', 'horizontal', 'vertical')

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    layout : :class:`Layout`

    linkingId : string

    orientation : :class:`Orientation`

    spacing : float

    static : boolean

    style : :class:`Style`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    yOffset : float

    """
    _schema = {'$ref': '#/definitions/MultipleViews'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, views=Undefined, arrangement=Undefined, assembly=Undefined,
                 centerRadius=Undefined, layout=Undefined, linkingId=Undefined, orientation=Undefined,
                 spacing=Undefined, static=Undefined, style=Undefined, xAxis=Undefined,
                 xDomain=Undefined, xOffset=Undefined, yOffset=Undefined, **kwds):
        super(MultipleViews, self).__init__(views=views, arrangement=arrangement, assembly=assembly,
                                            centerRadius=centerRadius, layout=layout,
                                            linkingId=linkingId, orientation=orientation,
                                            spacing=spacing, static=static, style=style, xAxis=xAxis,
                                            xDomain=xDomain, xOffset=xOffset, yOffset=yOffset, **kwds)


class MultivecData(DataDeep):
    """MultivecData schema wrapper

    Mapping(required=[type, url, column, row, value])

    Attributes
    ----------

    column : string

    row : string

    type : string

    url : string

    value : string

    binSize : float

    categories : List(string)

    end : string

    start : string

    """
    _schema = {'$ref': '#/definitions/MultivecData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, column=Undefined, row=Undefined, type=Undefined, url=Undefined, value=Undefined,
                 binSize=Undefined, categories=Undefined, end=Undefined, start=Undefined, **kwds):
        super(MultivecData, self).__init__(column=column, row=row, type=type, url=url, value=value,
                                           binSize=binSize, categories=categories, end=end, start=start,
                                           **kwds)


class OneOfFilter(FilterTransform):
    """OneOfFilter schema wrapper

    Mapping(required=[type, field, oneOf])

    Attributes
    ----------

    field : string

    oneOf : anyOf(List(string), List(float))

    type : string

    not : boolean

    """
    _schema = {'$ref': '#/definitions/OneOfFilter'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, oneOf=Undefined, type=Undefined, **kwds):
        super(OneOfFilter, self).__init__(field=field, oneOf=oneOf, type=type, **kwds)


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

    _renderingId : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    color : :class:`Channel`

    column : :class:`Channel`

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    encoding : Mapping(required=[])

    endAngle : float

    flipY : boolean

    height : float

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    mark : :class:`Mark`

    opacity : :class:`Channel`

    orientation : :class:`Orientation`

    outerRadius : float

    overlay : List(Mapping(required=[]))

    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])

    row : :class:`Channel`

    size : :class:`Channel`

    spacing : float

    startAngle : float

    static : boolean

    stretch : boolean

    stroke : :class:`Channel`

    strokeWidth : :class:`Channel`

    style : :class:`Style`

    subtitle : string

    template : string

    text : :class:`Channel`

    title : string

    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    width : float

    x : :class:`Channel`

    x1 : :class:`Channel`

    x1e : :class:`Channel`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    xe : :class:`Channel`

    y : :class:`Channel`

    y1 : :class:`Channel`

    y1e : :class:`Channel`

    yOffset : float

    ye : :class:`Channel`

    """
    _schema = {'$ref': '#/definitions/PartialTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, color=Undefined, column=Undefined, data=Undefined,
                 dataTransform=Undefined, displacement=Undefined, encoding=Undefined,
                 endAngle=Undefined, flipY=Undefined, height=Undefined, id=Undefined,
                 innerRadius=Undefined, layout=Undefined, linkingId=Undefined, mark=Undefined,
                 opacity=Undefined, orientation=Undefined, outerRadius=Undefined, overlay=Undefined,
                 overlayOnPreviousTrack=Undefined, overrideTemplate=Undefined, prerelease=Undefined,
                 row=Undefined, size=Undefined, spacing=Undefined, startAngle=Undefined,
                 static=Undefined, stretch=Undefined, stroke=Undefined, strokeWidth=Undefined,
                 style=Undefined, subtitle=Undefined, template=Undefined, text=Undefined,
                 title=Undefined, tooltip=Undefined, visibility=Undefined, width=Undefined, x=Undefined,
                 x1=Undefined, x1e=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined,
                 xe=Undefined, y=Undefined, y1=Undefined, y1e=Undefined, yOffset=Undefined,
                 ye=Undefined, **kwds):
        super(PartialTrack, self).__init__(_invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                           assembly=assembly, centerRadius=centerRadius, color=color,
                                           column=column, data=data, dataTransform=dataTransform,
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
                                           y1=y1, y1e=y1e, yOffset=yOffset, ye=ye, **kwds)


class Range(GoslingSchema):
    """Range schema wrapper

    anyOf(List(string), List(float), :class:`PREDEFINED_COLORS`)
    """
    _schema = {'$ref': '#/definitions/Range'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(Range, self).__init__(*args, **kwds)


class PREDEFINED_COLORS(Range):
    """PREDEFINED_COLORS schema wrapper

    enum('viridis', 'grey', 'spectral', 'warm', 'cividis', 'bupu', 'rdbu')
    """
    _schema = {'$ref': '#/definitions/PREDEFINED_COLORS'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args):
        super(PREDEFINED_COLORS, self).__init__(*args)


class RangeFilter(FilterTransform):
    """RangeFilter schema wrapper

    Mapping(required=[type, field, inRange])

    Attributes
    ----------

    field : string

    inRange : List(float)

    type : string

    not : boolean

    """
    _schema = {'$ref': '#/definitions/RangeFilter'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, field=Undefined, inRange=Undefined, type=Undefined, **kwds):
        super(RangeFilter, self).__init__(field=field, inRange=inRange, type=type, **kwds)


class RootSpecWithMultipleViews(GoslingSpec):
    """RootSpecWithMultipleViews schema wrapper

    Mapping(required=[views])

    Attributes
    ----------

    views : List(anyOf(:class:`SingleView`, :class:`MultipleViews`))

    arrangement : enum('parallel', 'serial', 'horizontal', 'vertical')

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    description : string

    layout : :class:`Layout`

    linkingId : string

    orientation : :class:`Orientation`

    spacing : float

    static : boolean

    style : :class:`Style`

    subtitle : string

    title : string

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    yOffset : float

    """
    _schema = {'$ref': '#/definitions/RootSpecWithMultipleViews'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, views=Undefined, arrangement=Undefined, assembly=Undefined,
                 centerRadius=Undefined, description=Undefined, layout=Undefined, linkingId=Undefined,
                 orientation=Undefined, spacing=Undefined, static=Undefined, style=Undefined,
                 subtitle=Undefined, title=Undefined, xAxis=Undefined, xDomain=Undefined,
                 xOffset=Undefined, yOffset=Undefined, **kwds):
        super(RootSpecWithMultipleViews, self).__init__(views=views, arrangement=arrangement,
                                                        assembly=assembly, centerRadius=centerRadius,
                                                        description=description, layout=layout,
                                                        linkingId=linkingId, orientation=orientation,
                                                        spacing=spacing, static=static, style=style,
                                                        subtitle=subtitle, title=title, xAxis=xAxis,
                                                        xDomain=xDomain, xOffset=xOffset,
                                                        yOffset=yOffset, **kwds)


class RootSpecWithSingleView(GoslingSpec):
    """RootSpecWithSingleView schema wrapper

    anyOf(Mapping(required=[alignment, height, tracks, width]), Mapping(required=[tracks]),
    Mapping(required=[tracks]))
    """
    _schema = {'$ref': '#/definitions/RootSpecWithSingleView'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, *args, **kwds):
        super(RootSpecWithSingleView, self).__init__(*args, **kwds)


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

    centerRadius : float
        Proportion of the radius of the center white space.
    layout : :class:`Layout`

    linkingId : string

    orientation : :class:`Orientation`

    spacing : float

    static : boolean

    style : :class:`Style`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    yOffset : float

    """
    _schema = {'$ref': '#/definitions/FlatTracks'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, tracks=Undefined, assembly=Undefined, centerRadius=Undefined, layout=Undefined,
                 linkingId=Undefined, orientation=Undefined, spacing=Undefined, static=Undefined,
                 style=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined,
                 yOffset=Undefined, **kwds):
        super(FlatTracks, self).__init__(tracks=tracks, assembly=assembly, centerRadius=centerRadius,
                                         layout=layout, linkingId=linkingId, orientation=orientation,
                                         spacing=spacing, static=static, style=style, xAxis=xAxis,
                                         xDomain=xDomain, xOffset=xOffset, yOffset=yOffset, **kwds)


class OverlaidTracks(SingleView):
    """OverlaidTracks schema wrapper

    Mapping(required=[alignment, tracks, width, height])

    Attributes
    ----------

    alignment : string

    height : float

    tracks : List(:class:`PartialTrack`)

    width : float

    _invalidTrack : boolean

    _renderingId : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    color : :class:`Channel`

    column : :class:`Channel`

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float

    flipY : boolean

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    mark : :class:`Mark`

    opacity : :class:`Channel`

    orientation : :class:`Orientation`

    outerRadius : float

    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])

    row : :class:`Channel`

    size : :class:`Channel`

    spacing : float

    startAngle : float

    static : boolean

    stretch : boolean

    stroke : :class:`Channel`

    strokeWidth : :class:`Channel`

    style : :class:`Style`

    subtitle : string

    text : :class:`Channel`

    title : string

    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    x : :class:`Channel`

    x1 : :class:`Channel`

    x1e : :class:`Channel`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    xe : :class:`Channel`

    y : :class:`Channel`

    y1 : :class:`Channel`

    y1e : :class:`Channel`

    yOffset : float

    ye : :class:`Channel`

    """
    _schema = {'$ref': '#/definitions/OverlaidTracks'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, alignment=Undefined, height=Undefined, tracks=Undefined, width=Undefined,
                 _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, color=Undefined, column=Undefined, data=Undefined,
                 dataTransform=Undefined, displacement=Undefined, endAngle=Undefined, flipY=Undefined,
                 id=Undefined, innerRadius=Undefined, layout=Undefined, linkingId=Undefined,
                 mark=Undefined, opacity=Undefined, orientation=Undefined, outerRadius=Undefined,
                 overlayOnPreviousTrack=Undefined, overrideTemplate=Undefined, prerelease=Undefined,
                 row=Undefined, size=Undefined, spacing=Undefined, startAngle=Undefined,
                 static=Undefined, stretch=Undefined, stroke=Undefined, strokeWidth=Undefined,
                 style=Undefined, subtitle=Undefined, text=Undefined, title=Undefined,
                 tooltip=Undefined, visibility=Undefined, x=Undefined, x1=Undefined, x1e=Undefined,
                 xAxis=Undefined, xDomain=Undefined, xOffset=Undefined, xe=Undefined, y=Undefined,
                 y1=Undefined, y1e=Undefined, yOffset=Undefined, ye=Undefined, **kwds):
        super(OverlaidTracks, self).__init__(alignment=alignment, height=height, tracks=tracks,
                                             width=width, _invalidTrack=_invalidTrack,
                                             _renderingId=_renderingId, assembly=assembly,
                                             centerRadius=centerRadius, color=color, column=column,
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
                                             y1e=y1e, yOffset=yOffset, ye=ye, **kwds)


class StackedTracks(SingleView):
    """StackedTracks schema wrapper

    Mapping(required=[tracks])

    Attributes
    ----------

    tracks : List(anyOf(:class:`PartialTrack`, :class:`OverlaidTracks`))

    _invalidTrack : boolean

    _renderingId : string

    alignment : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    color : :class:`Channel`

    column : :class:`Channel`

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float

    flipY : boolean

    height : float

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    mark : :class:`Mark`

    opacity : :class:`Channel`

    orientation : :class:`Orientation`

    outerRadius : float

    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])

    row : :class:`Channel`

    size : :class:`Channel`

    spacing : float

    startAngle : float

    static : boolean

    stretch : boolean

    stroke : :class:`Channel`

    strokeWidth : :class:`Channel`

    style : :class:`Style`

    subtitle : string

    text : :class:`Channel`

    title : string

    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    width : float

    x : :class:`Channel`

    x1 : :class:`Channel`

    x1e : :class:`Channel`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    xe : :class:`Channel`

    y : :class:`Channel`

    y1 : :class:`Channel`

    y1e : :class:`Channel`

    yOffset : float

    ye : :class:`Channel`

    """
    _schema = {'$ref': '#/definitions/StackedTracks'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, tracks=Undefined, _invalidTrack=Undefined, _renderingId=Undefined,
                 alignment=Undefined, assembly=Undefined, centerRadius=Undefined, color=Undefined,
                 column=Undefined, data=Undefined, dataTransform=Undefined, displacement=Undefined,
                 endAngle=Undefined, flipY=Undefined, height=Undefined, id=Undefined,
                 innerRadius=Undefined, layout=Undefined, linkingId=Undefined, mark=Undefined,
                 opacity=Undefined, orientation=Undefined, outerRadius=Undefined,
                 overlayOnPreviousTrack=Undefined, overrideTemplate=Undefined, prerelease=Undefined,
                 row=Undefined, size=Undefined, spacing=Undefined, startAngle=Undefined,
                 static=Undefined, stretch=Undefined, stroke=Undefined, strokeWidth=Undefined,
                 style=Undefined, subtitle=Undefined, text=Undefined, title=Undefined,
                 tooltip=Undefined, visibility=Undefined, width=Undefined, x=Undefined, x1=Undefined,
                 x1e=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined, xe=Undefined,
                 y=Undefined, y1=Undefined, y1e=Undefined, yOffset=Undefined, ye=Undefined, **kwds):
        super(StackedTracks, self).__init__(tracks=tracks, _invalidTrack=_invalidTrack,
                                            _renderingId=_renderingId, alignment=alignment,
                                            assembly=assembly, centerRadius=centerRadius, color=color,
                                            column=column, data=data, dataTransform=dataTransform,
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
                                            y1=y1, y1e=y1e, yOffset=yOffset, ye=ye, **kwds)


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


class Style(GoslingSchema):
    """Style schema wrapper

    Mapping(required=[])

    Attributes
    ----------

    align : enum('left', 'right')

    background : string

    backgroundOpacity : float

    bazierLink : boolean

    circularLink : boolean

    curve : enum('top', 'bottom', 'left', 'right')

    dashed : List([float, float])

    dx : float

    dy : float

    enableSmoothPath : boolean

    inlineLegend : boolean

    legendTitle : string

    linePattern : Mapping(required=[type, size])

    linkConnectionType : enum('straight', 'curve', 'corner')

    outline : string

    outlineWidth : float

    textAnchor : enum('start', 'middle', 'end')

    textFontSize : float

    textFontWeight : enum('bold', 'normal')

    textStroke : string

    textStrokeWidth : float

    """
    _schema = {'$ref': '#/definitions/Style'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                 bazierLink=Undefined, circularLink=Undefined, curve=Undefined, dashed=Undefined,
                 dx=Undefined, dy=Undefined, enableSmoothPath=Undefined, inlineLegend=Undefined,
                 legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                 outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                 textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                 textStrokeWidth=Undefined, **kwds):
        super(Style, self).__init__(align=align, background=background,
                                    backgroundOpacity=backgroundOpacity, bazierLink=bazierLink,
                                    circularLink=circularLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                                    enableSmoothPath=enableSmoothPath, inlineLegend=inlineLegend,
                                    legendTitle=legendTitle, linePattern=linePattern,
                                    linkConnectionType=linkConnectionType, outline=outline,
                                    outlineWidth=outlineWidth, textAnchor=textAnchor,
                                    textFontSize=textFontSize, textFontWeight=textFontWeight,
                                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)


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

    width : float

    _invalidTrack : boolean

    _renderingId : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    endAngle : float

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    orientation : :class:`Orientation`

    outerRadius : float

    overlayOnPreviousTrack : boolean

    prerelease : Mapping(required=[])

    spacing : float

    startAngle : float

    static : boolean

    style : :class:`Style`

    subtitle : string

    title : string

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    yOffset : float

    """
    _schema = {'$ref': '#/definitions/DataTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, data=Undefined, height=Undefined, width=Undefined, _invalidTrack=Undefined,
                 _renderingId=Undefined, assembly=Undefined, centerRadius=Undefined, endAngle=Undefined,
                 id=Undefined, innerRadius=Undefined, layout=Undefined, linkingId=Undefined,
                 orientation=Undefined, outerRadius=Undefined, overlayOnPreviousTrack=Undefined,
                 prerelease=Undefined, spacing=Undefined, startAngle=Undefined, static=Undefined,
                 style=Undefined, subtitle=Undefined, title=Undefined, xAxis=Undefined,
                 xDomain=Undefined, xOffset=Undefined, yOffset=Undefined, **kwds):
        super(DataTrack, self).__init__(data=data, height=height, width=width,
                                        _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                        assembly=assembly, centerRadius=centerRadius, endAngle=endAngle,
                                        id=id, innerRadius=innerRadius, layout=layout,
                                        linkingId=linkingId, orientation=orientation,
                                        outerRadius=outerRadius,
                                        overlayOnPreviousTrack=overlayOnPreviousTrack,
                                        prerelease=prerelease, spacing=spacing, startAngle=startAngle,
                                        static=static, style=style, subtitle=subtitle, title=title,
                                        xAxis=xAxis, xDomain=xDomain, xOffset=xOffset, yOffset=yOffset,
                                        **kwds)


class OverlaidTrack(Track):
    """OverlaidTrack schema wrapper

    Mapping(required=[height, overlay, width])
    Superposing multiple tracks.

    Attributes
    ----------

    height : float

    overlay : List(Mapping(required=[]))

    width : float

    _invalidTrack : boolean

    _renderingId : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    color : :class:`Channel`

    column : :class:`Channel`

    data : :class:`DataDeep`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float

    flipY : boolean

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    mark : :class:`Mark`

    opacity : :class:`Channel`

    orientation : :class:`Orientation`

    outerRadius : float

    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])

    row : :class:`Channel`

    size : :class:`Channel`

    spacing : float

    startAngle : float

    static : boolean

    stretch : boolean

    stroke : :class:`Channel`

    strokeWidth : :class:`Channel`

    style : :class:`Style`

    subtitle : string

    text : :class:`Channel`

    title : string

    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    x : :class:`Channel`

    x1 : :class:`Channel`

    x1e : :class:`Channel`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    xe : :class:`Channel`

    y : :class:`Channel`

    y1 : :class:`Channel`

    y1e : :class:`Channel`

    yOffset : float

    ye : :class:`Channel`

    """
    _schema = {'$ref': '#/definitions/OverlaidTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, height=Undefined, overlay=Undefined, width=Undefined, _invalidTrack=Undefined,
                 _renderingId=Undefined, assembly=Undefined, centerRadius=Undefined, color=Undefined,
                 column=Undefined, data=Undefined, dataTransform=Undefined, displacement=Undefined,
                 endAngle=Undefined, flipY=Undefined, id=Undefined, innerRadius=Undefined,
                 layout=Undefined, linkingId=Undefined, mark=Undefined, opacity=Undefined,
                 orientation=Undefined, outerRadius=Undefined, overlayOnPreviousTrack=Undefined,
                 overrideTemplate=Undefined, prerelease=Undefined, row=Undefined, size=Undefined,
                 spacing=Undefined, startAngle=Undefined, static=Undefined, stretch=Undefined,
                 stroke=Undefined, strokeWidth=Undefined, style=Undefined, subtitle=Undefined,
                 text=Undefined, title=Undefined, tooltip=Undefined, visibility=Undefined, x=Undefined,
                 x1=Undefined, x1e=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined,
                 xe=Undefined, y=Undefined, y1=Undefined, y1e=Undefined, yOffset=Undefined,
                 ye=Undefined, **kwds):
        super(OverlaidTrack, self).__init__(height=height, overlay=overlay, width=width,
                                            _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                            assembly=assembly, centerRadius=centerRadius, color=color,
                                            column=column, data=data, dataTransform=dataTransform,
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
                                            y1e=y1e, yOffset=yOffset, ye=ye, **kwds)


class SingleTrack(Track):
    """SingleTrack schema wrapper

    Mapping(required=[data, height, mark, width])

    Attributes
    ----------

    data : :class:`DataDeep`

    height : float

    mark : :class:`Mark`

    width : float

    _invalidTrack : boolean

    _renderingId : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    color : :class:`Channel`

    column : :class:`Channel`

    dataTransform : List(:class:`DataTransform`)

    displacement : :class:`Displacement`

    endAngle : float

    flipY : boolean

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    opacity : :class:`Channel`

    orientation : :class:`Orientation`

    outerRadius : float

    overlayOnPreviousTrack : boolean

    overrideTemplate : boolean

    prerelease : Mapping(required=[])

    row : :class:`Channel`

    size : :class:`Channel`

    spacing : float

    startAngle : float

    static : boolean

    stretch : boolean

    stroke : :class:`Channel`

    strokeWidth : :class:`Channel`

    style : :class:`Style`

    subtitle : string

    text : :class:`Channel`

    title : string

    tooltip : List(:class:`Tooltip`)

    visibility : List(:class:`VisibilityCondition`)

    x : :class:`Channel`

    x1 : :class:`Channel`

    x1e : :class:`Channel`

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    xe : :class:`Channel`

    y : :class:`Channel`

    y1 : :class:`Channel`

    y1e : :class:`Channel`

    yOffset : float

    ye : :class:`Channel`

    """
    _schema = {'$ref': '#/definitions/SingleTrack'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, data=Undefined, height=Undefined, mark=Undefined, width=Undefined,
                 _invalidTrack=Undefined, _renderingId=Undefined, assembly=Undefined,
                 centerRadius=Undefined, color=Undefined, column=Undefined, dataTransform=Undefined,
                 displacement=Undefined, endAngle=Undefined, flipY=Undefined, id=Undefined,
                 innerRadius=Undefined, layout=Undefined, linkingId=Undefined, opacity=Undefined,
                 orientation=Undefined, outerRadius=Undefined, overlayOnPreviousTrack=Undefined,
                 overrideTemplate=Undefined, prerelease=Undefined, row=Undefined, size=Undefined,
                 spacing=Undefined, startAngle=Undefined, static=Undefined, stretch=Undefined,
                 stroke=Undefined, strokeWidth=Undefined, style=Undefined, subtitle=Undefined,
                 text=Undefined, title=Undefined, tooltip=Undefined, visibility=Undefined, x=Undefined,
                 x1=Undefined, x1e=Undefined, xAxis=Undefined, xDomain=Undefined, xOffset=Undefined,
                 xe=Undefined, y=Undefined, y1=Undefined, y1e=Undefined, yOffset=Undefined,
                 ye=Undefined, **kwds):
        super(SingleTrack, self).__init__(data=data, height=height, mark=mark, width=width,
                                          _invalidTrack=_invalidTrack, _renderingId=_renderingId,
                                          assembly=assembly, centerRadius=centerRadius, color=color,
                                          column=column, dataTransform=dataTransform,
                                          displacement=displacement, endAngle=endAngle, flipY=flipY,
                                          id=id, innerRadius=innerRadius, layout=layout,
                                          linkingId=linkingId, opacity=opacity, orientation=orientation,
                                          outerRadius=outerRadius,
                                          overlayOnPreviousTrack=overlayOnPreviousTrack,
                                          overrideTemplate=overrideTemplate, prerelease=prerelease,
                                          row=row, size=size, spacing=spacing, startAngle=startAngle,
                                          static=static, stretch=stretch, stroke=stroke,
                                          strokeWidth=strokeWidth, style=style, subtitle=subtitle,
                                          text=text, title=title, tooltip=tooltip,
                                          visibility=visibility, x=x, x1=x1, x1e=x1e, xAxis=xAxis,
                                          xDomain=xDomain, xOffset=xOffset, xe=xe, y=y, y1=y1, y1e=y1e,
                                          yOffset=yOffset, ye=ye, **kwds)


class TemplateTrack(Track):
    """TemplateTrack schema wrapper

    Mapping(required=[data, height, template, width])
    Template specification that will be internally converted into `SingleTrack` for rendering

    Attributes
    ----------

    data : :class:`DataDeep`

    height : float

    template : string

    width : float

    _invalidTrack : boolean

    _renderingId : string

    assembly : :class:`Assembly`

    centerRadius : float
        Proportion of the radius of the center white space.
    encoding : Mapping(required=[])

    endAngle : float

    id : string

    innerRadius : float

    layout : :class:`Layout`

    linkingId : string

    orientation : :class:`Orientation`

    outerRadius : float

    overlayOnPreviousTrack : boolean

    prerelease : Mapping(required=[])

    spacing : float

    startAngle : float

    static : boolean

    style : :class:`Style`

    subtitle : string

    title : string

    xAxis : :class:`AxisPosition`

    xDomain : anyOf(:class:`DomainInterval`, :class:`DomainChrInterval`, :class:`DomainChr`)

    xOffset : float

    yOffset : float

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
                 xOffset=Undefined, yOffset=Undefined, **kwds):
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
                                            xDomain=xDomain, xOffset=xOffset, yOffset=yOffset, **kwds)


class VectorData(DataDeep):
    """VectorData schema wrapper

    Mapping(required=[type, url, column, value])

    Attributes
    ----------

    column : string

    type : string

    url : string

    value : string

    binSize : float

    end : string

    start : string

    """
    _schema = {'$ref': '#/definitions/VectorData'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, column=Undefined, type=Undefined, url=Undefined, value=Undefined,
                 binSize=Undefined, end=Undefined, start=Undefined, **kwds):
        super(VectorData, self).__init__(column=column, type=type, url=url, value=value,
                                         binSize=binSize, end=end, start=start, **kwds)


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

    operation : :class:`LogicalOperation`

    target : enum('track', 'mark')

    threshold : anyOf(float, string)

    conditionPadding : float

    transitionPadding : float

    """
    _schema = {'$ref': '#/definitions/SizeVisibilityCondition'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, measure=Undefined, operation=Undefined, target=Undefined, threshold=Undefined,
                 conditionPadding=Undefined, transitionPadding=Undefined, **kwds):
        super(SizeVisibilityCondition, self).__init__(measure=measure, operation=operation,
                                                      target=target, threshold=threshold,
                                                      conditionPadding=conditionPadding,
                                                      transitionPadding=transitionPadding, **kwds)


class ZoomLevelVisibilityCondition(VisibilityCondition):
    """ZoomLevelVisibilityCondition schema wrapper

    Mapping(required=[measure, operation, target, threshold])

    Attributes
    ----------

    measure : string

    operation : :class:`LogicalOperation`

    target : enum('track', 'mark')

    threshold : float

    conditionPadding : float

    transitionPadding : float

    """
    _schema = {'$ref': '#/definitions/ZoomLevelVisibilityCondition'}
    _rootschema = GoslingSchema._rootschema

    def __init__(self, measure=Undefined, operation=Undefined, target=Undefined, threshold=Undefined,
                 conditionPadding=Undefined, transitionPadding=Undefined, **kwds):
        super(ZoomLevelVisibilityCondition, self).__init__(measure=measure, operation=operation,
                                                           target=target, threshold=threshold,
                                                           conditionPadding=conditionPadding,
                                                           transitionPadding=transitionPadding, **kwds)

