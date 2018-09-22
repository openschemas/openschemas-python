# Copyright (c) 2018, Vanessa Sochat All rights reserved.
# See the LICENSE in the main repository at:
#    https://www.github.com/openschemas/openschemas-python

from rdflib import ConjunctiveGraph
import csv
import os
import re
import requests
import sys

# Loading Functions

def load_tsv(filename):
    '''load a tsv file using the csv default provided reader!

       Parameters
       ==========
       filename: the file name to load, will return list (rows) of
       lists (columns)
    '''
    rows = []
    with open(filename,'r') as tsv:
        content = csv.reader(tsv, delimiter='\t')
        for row in content:
            if row:
                rows.append(row)

    return rows


# RDF Functions

def __get_class_name(temp_uri):
    return temp_uri.replace("http://schema.org/","")


def __add_property(props_dic, prop_desc):
    sdo_uri="http://schema.org/"
    if prop_desc['prop_name'] in props_dic:
        t_prop_name = prop_desc['prop_name']
        props_dic[t_prop_name]['exp_type'].append(prop_desc['exp_type'].replace(sdo_uri,""))
    else:
        props_dic[prop_desc['prop_name']]=prop_desc
        props_dic[prop_desc['prop_name']]['exp_type'] = [prop_desc['exp_type'].replace(sdo_uri,"")]
    return props_dic


def __get_class_props(class_name, graph):
    print("Quering properties of %s in Schema.org" % class_name)

    qres = graph.query("""prefix schema: <http://schema.org/>
                        select distinct * where {
                            ?property schema:domainIncludes  schema:%s .
                            ?property schema:rangeIncludes  ?exp_type .
                            ?property rdfs:label ?prop_name.
                            ?property rdfs:comment ?description
                        }""" % class_name)
    temp_dic = {}

    for row in qres:
        labels=row.labels.keys()
        labels_dic = {}
        for label in labels:
            labels_dic[label] = str(row[label]).replace('<a href=\"/docs/', '<a href=\"http://schema.org/docs/')
        temp_dic=__add_property(temp_dic, labels_dic)

    return temp_dic


def __get_parent_type(class_name, graph):

    print("Find parent type of %s in Schema.org" % class_name)

    qres = graph.query("""prefix schema: <http://schema.org/>
                          select ?supclass where{
                          ?class rdfs:label ?label .
                          ?class rdfs:subClassOf ?supclass .
                          filter (?label='%s')
                        }""" % class_name)
    resp_arr=[]

    for row in qres:
        resp_arr.append(str(row['supclass']))
    return resp_arr[0].replace('http://schema.org/', '')


def _get_properties(class_name, graph, properties):

    if class_name == 'Thing':
        properties[class_name] = __get_class_props(class_name, graph)
        return properties
    else:
        temp_props = __get_class_props(class_name, graph)
        properties[class_name] = temp_props
        parent_type = __get_parent_type(class_name, graph)
        _get_properties(parent_type, graph, properties)


def get_properties_in_hierarchy(type_name):
    query_type = type_name
    g = ConjunctiveGraph()
    g.parse('http://schema.org/version/latest/schema.jsonld', format='json-ld')
    props_dic={}
    _get_properties(query_type, g, props_dic)
    return props_dic


def get_hierarchy(props_dic):
    type_hierarchy = []
    for h_type in props_dic:
        type_hierarchy.append(h_type)
    return type_hierarchy


def get_expected_types(expected_types):
    '''Function that receives an string with expected types
       and generates an array with each expected type
    '''
    # Get rid of newlines anywhere
    expected_types = expected_types.strip().replace('\n',' ')

    # Get rid of OR in any casing, anywhere with space either side
    expected_types = re.sub(' (o|O)(r|R) ', ' ', expected_types)

    # Split based on space OR comma
    expected_types = re.split(' |,', expected_types)

    # Keep a separate final list of cleaned types
    list_of_types = []

    for expected_type in expected_types:
        if expected_type not in ['', None]:
            list_of_types.append(expected_type.strip())

    return list_of_types

def get_row_value(field, row, headers, default='', clean=True):
    '''get a value from a list based on a field name that is expected to 
       appear in headers. This allows for change in the ordering of fields
       as long as the header is correctly labeled. The default value of
       an empty string is returned, and we clean by stripping spaces and
       newlines.

       Parameters
       ==========
       field: the field to look up
       row: the row (list) of values
       headers: the list of field names (header of the tsv file) to match field
       default: the default value to return, if not found
       clean: boolean to indicate wanting to strip newlines and spaces
    '''
    value = default
    for i in range(0, len(row)):
        if headers[i] == field:
            value = row[i]
            break
    
    if clean is True:
        value = value.strip().replace('\n', '')
    return value

def get_dict_from_row(row, headers):
    '''a row is typically a list of values, assigned to another list of headers.
       this function parses a known set of headers and enters them into
       the expected values for bioschemas attributes. We return a dict.
 
       Properties
       ==========
       row: the row (list) of values from the bioschemas tsv file
       headers: the headers that are expected (already validated)
    '''
    props = {}

    # Set Bioschemas attributes
    props['bsc_description'] = get_row_value('BSC Description', row, headers)
    props['cardinality'] = get_row_value('Cardinality', row, headers)
    props['controlled_vocab'] = get_row_value('Controlled Vocabulary', row, headers)
    props['description'] = get_row_value('Description', row, headers, ' ')
    props['example'] = get_row_value('Example', row, headers)
    props['marginality'] = get_row_value('Marginality', row, headers)
    props['property'] = get_row_value('Property', row, headers)
    props['type'] = get_row_value('Type', row, headers)
    props['type_url'] = get_row_value('Type URL', row, headers)

    # Expected types list, cleaned up
    expected_types = get_row_value('Expected Type', row, headers)
    props['expected_types'] = get_expected_types(expected_types)

    return props


def get_property_in_hierarchy(sdo_props, mapping_property, prop_type="new_sdo"):
    '''if a mapping property (indexed by its name, which is key "property")
       if found as a key in sdo_props at a particular entity (e.g., Thing)
       then we've found it in the sdo, and grab it's description for use from
       the sdo. If we don't find it, we return the type as a "new_sdo"
    '''
    for entity in sdo_props:
        if mapping_property['property'] in sdo_props[entity]:
            prop_type = entity
            name = mapping_property['property']
            desc = sdo_props[entity][name]['description']
            mapping_property['description'] = desc
            break

    return {'type': prop_type, 
            'property': mapping_property}


def get_formatted_props(sdo_props, 
                        mapping_props,
                        spec_name, 
                        spec_type):
    '''This function combines the parsed mapping properties (importantly, 
       mapping_props needs to "parent" field added) with the properties
       from the standard ontology
 
       ::Note: this function needs testing for a type

       Parameters
       ==========
       sdo_props: standard ontology (shared) properties
       mapping_props: result from get_mapping_properties (bioschemas_file)
       spec_name: the name of the specification (specification_file)
       spec_type: the type of the specification (specification_file)
    '''

    all_props= []
    bsc_props = []

    # if "Type" only get new properties from mapping file
    if(spec_type.lower() == "type"):

        for mapping_property in mapping_props:

            bsc_props.append(mapping_property['property'])
            temp_prop = get_property_in_hierarchy(sdo_props, mapping_property)
            if temp_prop['type'] == "new_sdo":
                temp_prop['property']['parent'] = spec_name
            all_props.append(temp_prop['property'])

        for sdo_prop in sdo_props:

            # now get all props from schema & make them such that _layout can use them
            for sdo_prop_prop in sdo_props[sdo_prop].keys():
                if sdo_props[sdo_prop][sdo_prop_prop]['prop_name'] not in bsc_props:
                    sdo_props[sdo_prop][sdo_prop_prop]['parent'] = sdo_prop
                    sdo_props[sdo_prop][sdo_prop_prop]['property'] = sdo_props[sdo_prop][sdo_prop_prop]['prop_name']
                    # sdo_props[sdo_prop][sdo_prop_prop]['bsc_dec'] = sdo_props[sdo_prop][sdo_prop_prop]['description']
                    sdo_props[sdo_prop][sdo_prop_prop]['description'] = sdo_props[sdo_prop][sdo_prop_prop]['description']
                    sdo_props[sdo_prop][sdo_prop_prop]['expected_type'] = sdo_props[sdo_prop][sdo_prop_prop]['exp_type']
                    all_props.append(sdo_props[sdo_prop][sdo_prop_prop])
                else:
                    for i in all_props:
                        if i['property'] == sdo_props[sdo_prop][sdo_prop_prop]['prop_name']:
                            i['parent'] = sdo_prop
        
    # if profile
    else:
        for mapping_prop in mapping_props:
            temp_prop = get_property_in_hierarchy(sdo_props, mapping_prop)
            if temp_prop['type'] == "new_sdo":
                temp_prop['property']['parent'] = spec_name
            else:
                temp_prop['property']['parent'] = temp_prop['type']
            all_props.append(temp_prop['property'])

    return all_props


def get_mapping_properties(bioschemas_file):
    '''get_mapping_properties
       use the bioschemas field file and the specification type to
       return a list of type properties. The bioschemas file 
       should already be validated for correct headers.

       Parameters
       ==========
       bioschemas_file: the <Template> - Bioschemas.tsv file
    '''

    rows = load_tsv(bioschemas_file)
    headers = rows[0]
    type_properties = []
    
    for r in range(1,len(rows)):
        row = rows[r]
        
        # If we want to do checks for empty cells, do it here

        # If Expected Type, Marginality, and Cardinaity isn't empty 
        if row[1] != "" and rows[6] != "" and rows[7] != "":
            property_dict = get_dict_from_row(row, headers)
            type_properties.append(property_dict)

    return type_properties


class MappingParser:
    metadata = {}

    def __init__(self, metadata=None):
        if metadata != None:
            self.metadata = metadata

    def set_metadata(self, metadata):
        self.metadata = metadata


    def check_url(self, spec_url):
        '''check_url doesn't exit if the address isn't found, etc.
           it just adds the string "err_404" as metadata given these cases.
        '''
        if spec_url is None: 
            return "err_404"

        response = requests.get(spec_url)
        if response.status_code == 404:
            return "err_404"
        else:
            return spec_url

    def get_description(self, spec_file=None):

        if not spec_file:
            spec_file = self.metadata['specification_file']

        # Read in both, these are already validated
        spec_sheet = load_tsv(spec_file)

        # Generate values in advance
        name = self.metadata['name']
        gh_base = 'https://github.com/openschemas/specifications/tree/master'
        use_cases_url = self.metadata['use_cases_url']

        description = {}
        description['name'] = name

        description['status'] = self.metadata['status']
        description['spec_type'] = self.metadata['spec_type']

        # Github Future Links
        description['gh_folder'] = '%s/%s' % (gh_base, name)
        description['gh_tasks'] = 'https://github.com/openschemas/specifications/labels/type%3A%20'+ name

        description['edit_url']='%s/%s/specification.html' % (gh_base, name)
        description['use_cases_url'] = self.check_url(use_cases_url)
        description['version'] = self.metadata['version']
        description['parent_type'] = self.metadata.get('parent_type', 'Thing')

        # Parse specification file
        description['subtitle'] = spec_sheet[1][1]
        description['description'] = spec_sheet[1][2]
        return description

    def get_mapping(self, spec_sheet=None, 
                          bioschemas_sheet=None):
        '''get a mapping, meanng the full properties given a specification sheet
           and a bioschemas sheet. If files aren't provided, the defaults defined
           at self.defaults.paths are used.

           Parameters
           ==========
           spec_sheet: the sheet with basic information (description, name, etc.)
           bioschemas_sheet: sheet (tsv) with bioschemas fields
        '''

        print("\nParsing %s =========" % self.metadata['name'])

        # Pull out description, name, type
        description = self.get_description(spec_sheet)
        name = description['name']
        spec_type = description['spec_type']

        if bioschemas_sheet is None:
            bioschemas_sheet = self.metadata['bioschemas_file']

        try:
            ptype = description['parent_type']
            sdo_props = get_properties_in_hierarchy(ptype)
        except IndexError as e:
            print('Error finding parent %s! Is %s a valid entity?' %ptype)
            sys.exit(1)

        description['hierarchy'] = get_hierarchy(sdo_props)
        description['hierarchy'].reverse()
        print_hierarchy = ' > '.join(description['hierarchy'])
        print("Prepared schema.org properties for hierarchy %s" % print_hierarchy)
        print("Classifing %s properties" % description['name'])
        mapping_props = get_mapping_properties(bioschemas_sheet)

        # Combine new specification with standard ontology to get final mapping
        description['mapping'] = get_formatted_props(sdo_props,
                                                     mapping_props,
                                                     spec_name = name,
                                                     spec_type = spec_type)


        return description
