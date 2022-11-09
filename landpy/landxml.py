import lxml.etree as et



class LandXML:
    def __init__(self, lxml=None, *args, **kwargs):
        self.doc = et.XML(lxml)
        self.xmlns = str('{'+self.doc.nsmap[None]+'}')
        self._surfaces = None

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
        surfs_list = []
        surfaces = LandXMLSurfs(parent=self) 
        return surfaces

class LandXMLSurfs:
    def __init__(self,parent = None,*args, **kwargs):
        
        self._surfs_ele = parent.find_element('Surfaces')
        self._surfs_dict = {}
        if self._surfs_ele is None:
            print('No surfaces in LandXML object')
        else:
            children = self._surfs_ele.getchildren()
            for child in children:
                surf = LandXMLSurf(parent=parent,surf_obj=child)
                surf_name = surf.sname
                self._surfs_dict[surf_name] = surf
    
    @property
    def surfaces_ele(self):
        return self._surfs_ele
    
    @surfaces_ele.setter
    def surfaces_ele(self,lxml_ele):
        self._surfs_ele = lxml_ele
    
    @property
    def surfaces_dict(self):
        return self._surfs_dict

class LandXMLSurf:
    
    def __init__(self,parent = None, surf_obj = None,*args, **kwargs):
        
        self.parent = parent
        self._surfName = surf_obj.attrib['name']
        self._surfDef = surf_obj.find(f'{parent.xmlns}Definition')
        self._surfType = surf_obj.find(f'{parent.xmlns}Definition').attrib['surfType']
        
    
    @property
    def sname(self):
        return self._surfName
    
    @sname.setter
    def sname(self,surfName):
        self._surfName = surfName    
    
    @property
    def sdefinition(self):
        return self._surfDef
    
    @sdefinition.setter
    def sdefinition(self,surfDef):
        self._surfDef = surfDef
    
    @property
    def stype(self):
        return self._surfType
    
    @stype.setter
    def stype(self,surfType):
        self._surfType = surfType

    def get_points(self):
        surf_element = self.sdefinition
        element_point_list = surf_element.find(f'{self.parent.xmlns}Pnts').getchildren()
        point_list = []
        for point in element_point_list:
            point_list.append([float(x) for x in point.text.split(' ')])
        return point_list
    
    def get_point_ids(self,zeroidx=True,check=True):
        surf_element = self.sdefinition
        element_point_list = surf_element.find(f'{self.parent.xmlns}Pnts').getchildren()
        point_id_list = []
        
        for point in element_point_list:
            id = point.attrib['id']
            point_id_list.append(int(id))
        
        if zeroidx:
            offset = point_id_list[0]
            list_off = [x-offset for x in point_id_list]
        else:
            list_off = point_id_list
        
        if check:
            if len(element_point_list) != list_off[-1]:
                for i,c in zip(list(range(len(element_point_list))),list_off):
                    if i != c:
                        print(f'WARNING, indexes are not matching! Fix the input file at ID value: {c}')
                        break
        return list_off,offset

    def get_number_of_points(self):
        return len(self.get_points())

    def get_cells(self,zero_index=True):
        surf_element = self.sdefinition
        surf_type = self.stype
        element_faces_list = surf_element.find(f'{self.parent.xmlns}Faces').getchildren()
        face_arr = []
        
        #ids in vtk are 0 offset
        if zero_index:
            _,offset = self.get_point_ids()
        else:
            offset = 0
        for face in element_faces_list:
            id_list = [int(x)-offset for x in face.text.split(' ')]
            if surf_type == 'TIN':
                padding = 3
            elif surf_type == 'grid':
                padding = 4
            id_list.insert(0,padding)
            face_arr.append(id_list)
        return face_arr,element_faces_list
    
    def get_number_of_cells(self):
        return len(self.get_cells()[1])

class LandXMLPoints:
    def __init__(self, *args, **kwargs):
        ...


class LandXMLPoint:
    ...
