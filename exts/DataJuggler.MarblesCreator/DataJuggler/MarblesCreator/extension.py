# Important!!!!!!!!
# Important!!!!!!!!
# Important!!!!!!!!
# The images folder is now set via a StringField in the UI. Make sure the folder exists and has your images
# before clicking the Create Marbles button.
# To change the default folder, change line 41. 
# this can be run more than once

import os
import omni.kit.commands
import omni.ext
import omni.ui as ui
from pxr import Gf, Sdf, Usd, UsdShade
import omni
import carb
import glob

# default width
default_col_width = 300

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class DatajugglerMarblesExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    

    def on_startup(self, ext_id):
        print("[DataJuggler.Marbles] DataJuggler Marbles startup")         
        
        self._window = ui.Window("Data Juggler Marbles Creator", width=300, height=300)

        self._images_model = ui.SimpleStringModel()
        
        # Important!!!!!!!!
        # Important!!!!!!!!
        # Important!!!!!!!!
        # Set the images folder            
        imagesFolder = "C:/Graphics/Marbles1/"

        # set the default value
        self._images_model.as_string = imagesFolder
        self._number = 0
        self._xlocation = 0
        self._ylocation = 500
        self._zlocation = 0

        def on_click():

            # 10 is fast. If you change both these numbers to 40, it takes about 10 minutes on my fast pc
            rows = 10
            columns = 10
            number = self._number
            xLocation = self._xlocation
            zLocation = self._zlocation
            yLocation = number + 500
            index = 0

            imagesFolder = self._images_model.as_string

            images = []
            for file in glob.glob(imagesFolder + "*.png"):
                images.append(file)

            for x in range (rows):

                yLocation = yLocation + 2

                xLocation = x * 2
                
                for z in range(columns):

                    zLocation = z * 2

                    # increment
                    number = number + 1
                    index = number - 1
                    
                    # reset the index in case of more marbles than images
                    index = index % len(images)

                    baseName = "/World/Sphere"
                    name = baseName                            
                    pbrBase = "/World/Looks/"
                    pbrName = pbrBase + "OmniPBR"
                    
                    if (number > 1):

                        if (number < 11):
                        
                            name = baseName + "_0" + str(number -1)
                            pbrName = pbrName + "_0" + str(number -1)
                        
                        else:

                            name = baseName + "_" + str(number -1)
                            pbrName = pbrName + "_" + str(number -1)
                        
                    # create prim
                    spherePath = omni.kit.commands.execute('CreateMeshPrimWithDefaultXform', prim_type='Sphere')
                    
                    # Select the new prim
                    # omni.kit.commands.execute('SelectPrimsCommand', old_selected_paths=[oldName], new_selected_paths=[name], expand_in_stage=False)

                    # set rigid body
                    omni.kit.commands.execute('SetRigidBody', path=Sdf.Path(name), approximationShape='convexHull', kinematic=False)

                    # print("PBRName: " + pbrName)
                    # print("name: " + name)

                    mtl_created_list = []
                    # Create a new material using OmniPBR.mdl
                    omni.kit.commands.execute("CreateAndBindMdlMaterialFromLibrary", mdl_name="OmniPBR.mdl", mtl_name="OmniPBR", mtl_created_list=mtl_created_list)

                    stage = omni.usd.get_context().get_stage()
                    mtl_prim = stage.GetPrimAtPath(pbrName)

                    # Create an OmniPBR
                    # omni.kit.commands.execute('CreateAndBindMdlMaterialFromLibrary', mdl_name='OmniPBR.mdl', mtl_name='OmniPBR', mtl_created_list=[pbrName], bind_selected_prims=[name])

                    # built the path
                    # path = "/World/Looks/" + pbrName + "/Shader.inputs:diffuse_texture"

                    # Assign an image to the PBR                            
                    # omni.kit.commands.execute('ChangeProperty', prop_path=Sdf.Path(path), value=Sdf.AssetPath('C:/Temp/Pink.png'), prev=None)
                    imagePath = images[index]

                    omni.usd.create_material_input(mtl_prim, "diffuse_texture", imagePath, Sdf.ValueTypeNames.Asset,)

                    omni.kit.commands.execute('TransformMultiPrimsSRTCpp', 
                        count=1,
                        paths=[name],
                        new_translations=[xLocation, yLocation, zLocation],
                        new_rotation_eulers=[0.0, 0.0, 0.0],
                        new_rotation_orders=[0, 1, 2],
                        new_scales=[.013, .013, .013],
                        old_translations=[0, 0.0, 0.0],
                        old_rotation_eulers=[0.0, 0.0, 0.0],
                        old_rotation_orders=[0, 1, 2],
                        old_scales=[1.0, 1.0, 1.0],
                        usd_context_name='',
                        time_code=0.0)
                    
                    # assign material
                    cube_prim = stage.GetPrimAtPath(name)
                    
                    # Bind the material to the prim
                    cube_mat_shade = UsdShade.Material(mtl_prim)


                    UsdShade.MaterialBindingAPI(cube_prim).Bind(cube_mat_shade, UsdShade.Tokens.strongerThanDescendants) 
            
            # store the values in case ran again
            self._xlocation = xLocation
            self._ylocation = yLocation
            self._zlocation = zLocation
            self._number = number
        
        with self._window.frame:       

            with ui.VStack():
                label = ui.Label("")
                
                # get a string field
                string_field = omni.ui.StringField(model=self._images_model, height=32, width=default_col_width, tooltip="Set The Output Folder")
                
                label.text = "Images Directory"

                ui.Button("Create Marbles", clicked_fn=on_click) 
                    

    def on_shutdown(self):
        print("[DataJuggler.Marbles] DataJuggler Marbles shutdown")

    
