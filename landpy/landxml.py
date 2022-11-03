import lxml.etree as et



class LandXML():
    def __init__(self, lxml=None, *args, **kwargs):
        self.doc = et.XML(lxml)
        self.xmlns = str('{'+self.doc.nsmap[None]+'}')

    def get_xmlns(self):
        return self.xmlns
    
    def find_element(self,key=None):
        return self.doc.find(f'{self.xmlns}{key}')
   
    @property
    def units(self):
        units_dict = {}
        units_ele = self.find_element('Units') 
        if units_ele == None:
            print('No units in LandXML object')
        else:
            units_sys_ele = units_ele.getchildren()[0]
            units_sys = units_sys_ele.tag.split(f'{self.xmlns}')[1]
            units_dict['unitSystem'] = units_sys
            units_dict.update(units_sys_ele.attrib)
            return units_dict   
    
    @property
    def app_info(self):
        appl_ele = self.find_element('Application') 
        if appl_ele == None:
            print('No application information in LandXML object')
            return
        else:
            return appl_ele.attrib   
    
    @property
    def prj_name(self):
        prj_ele = self.find_element('Project') 
        if prj_ele == None:
            print('Project without name')
            return
        else:
            return prj_ele.attrib['name']
    
    @property
    def surfaces(self):
        surfs_dict = {}
        surfs_ele = self.find_element('Surfaces') 
        if surfs_ele == None:
            print('No surfaces in LandXML object')
        else:
            children = surfs_ele.getchildren()
            for child in children:
                surf_name = child.attrib['name']
                surf_type = child.find(f'{self.xmlns}Definition').attrib['surfType']
                surfs_dict[surf_name] = {'surfDefinition': child.find(f'{self.xmlns}Definition'),'surfType': surf_type}
            return surfs_dict

    # This should be in a standalone surface class 
    def get_points(self,surf):
        surf_element = surf['surfDefinition']
        element_point_list = surf_element.find(f'{self.xmlns}Pnts').getchildren()
        point_arr = []
        for point in element_point_list:
            point_arr.append(tuple(float(x) for x in point.text.split(' ')))
        return(point_arr)
    
    def get_cells(self,surf, zero_ind=True):
        surf_element = surf['surfDefinition']
        element_faces_list = surf_element.find(f'{self.xmlns}Faces').getchildren()
        face_arr = []
        
        #ids in landxml are 1 indexed, in VTK 0 indexed. Use zero_ind to convert to 0 indexed systems

        if zero_ind:
            for face in element_faces_list:
                face_arr.append(tuple(int(x)-1 for x in face.text.split(' ')))
        else:
            for face in element_faces_list:
                face_arr.append(tuple(int(x) for x in face.text.split(' ')))
        return(face_arr)
