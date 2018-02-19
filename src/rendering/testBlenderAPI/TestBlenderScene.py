import bpy

import sys

boop = '/Users/matthew/Documents/MSc/Group_Project/Lobster/src/'
if not (boop in sys.path):
    sys.path.append(boop)

C = bpy.context
C.scene.render.engine = 'CYCLES'


import unittest


import rendering.BlenderAPI as bld


from rendering.BlenderAPI.BlenderScene import BlenderScene
from rendering.BlenderAPI.BlenderScene import BlenderRoom
from rendering.BlenderAPI.BlenderCamera import BlenderCamera
from rendering.BlenderAPI.BlenderLamps import BlenderLamp, BlenderSun




# def main():
#     my_room = BlenderRoom(10)
#     print(len(my_room.walls))
#     my_scene = BlenderScene(bpy.data)
#
# main()

class BlenderSceneTest(unittest.TestCase):


    def setUp(self):
        self.my_room = BlenderRoom(10)
        self.my_scene = BlenderScene(bpy.data)

    def test_room_has_correct_number_of_walls(self):
        number_of_walls = len(self.my_room.walls)
        self.assertEqual(number_of_walls, 6, "Room does not have 6 walls!")

    def test_room_deletes_properly(self):
        self.my_room.delete()
        walls_post_deletion = self.my_room.walls
        self.assertEqual(walls_post_deletion, [], "Walls were not deleted properly!")

    def test_scene_is_set_up_correctly(self):
        self.assertEqual(self.my_scene.lamps, [])
        self.assertEqual(self.my_scene.background, None)
        self.assertEqual(self.my_scene.objects_fixed, [])
        self.assertEqual(self.my_scene.objects_unfixed, [])
        self.assertEqual(self.my_scene.camera, None)
        self.assertEqual(self.my_scene.subject, None)
        self.assertEqual(self.my_scene.data, bpy.data)

    def test_add_camera(self):
        new_camera = BlenderCamera()
        self.my_scene.add_camera(new_camera)
        self.assertEqual(self.my_scene.camera, new_camera, "Camera was not successfully added to scene!")

    #Currently failing this test because line 57 in BlenderScene should be self.lamps
    def test_add_lamps(self):
        # Add one lamp and check that it is successfully added
        new_lamp_sun = BlenderSun(bpy.data.objects['Lamp'])
        self.my_scene.add_lamp(new_lamp_sun)
        self.assertEqual(self.my_scene.lamps[0], new_lamp_sun, "Lamp (sun) was not successfully added to scene!")
        # Add another lamp of a different type and check that it is successfully added; also verify that previous lamp is still in position
        new_lamp_point = BlenderPoint(bpy.data.objects['Lamp'])
        self.assertEqual(self.my_scene.lamps[0], new_lamp_sun, "Lamp (sun) was not retained when new lamp was added to scene!")
        self.assertEqual(self.my_scene.lamps[1], new_lamp_point, "Lamp (point) was not successfully added to scene!")


    # Currently failing test because delete assumes that everything would have been instantiated first
    def test_delete_all(self):
        self.my_scene.delete_all();
        # Everything should now be back to its original state
        self.assertEqual(self.my_scene.lamps, [])
        self.assertEqual(self.my_scene.background, None)
        self.assertEqual(self.my_scene.objects_fixed, [])
        self.assertEqual(self.my_scene.objects_unfixed, [])
        self.assertEqual(self.my_scene.camera, None)
        self.assertEqual(self.my_scene.subject, None)
        self.assertEqual(self.my_scene.data, bpy.data)

    # def test_add_background(self):
    #     new_background = TODO
    #     self.my_scene.add_background(new_background)
    #     self.assertEqual(self.my_scene.background, new_background, "Background was not successfully added to scene!")

    def test_add_subject(self):
        new_subject_cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
        self.my_scene.add_subject(new_subject_cube)
        self.assertEqual(self.my_scene.subject, new_subject_cube, "Subject (cube) was not successfully added to scene!")

    def test_add_object_fixed(self):
        new_room = BlenderRoom(10);
        self.my_scene.add_object_fixed(new_room)
        # Check that room was successfully added
        self.assertTrue(self.my_scene.objects_fixed[0] == new_room, "Fixed object (room) was not successfully added to scene!")
        # Check that one and only one object was added
        self.assertEqual(len(self.my_scene.objects_fixed), 1, "Incorrect number of elements in objects_fixed list")

    def test_add_object_unfixed(self):
        new_object_cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
        self.my_scene.add_object_unfixed(new_object_cube)
        # Check that the cube was successfully added
        self.assertEqual(self.my_scene.objects_unfixed[0], new_object_cube, "Subject (cube) was not successfully added to scene!")
        # Check that one and only one object was added
        self.assertEqual(len(self.my_scene.objects_unfixed), 1, "Incorrect number of elements in objects_fixed list")

    def test_render_creation(self):
        self.my_scene.render_to_file('render_test_1.jpg')
        import os.path
        self.assertTrue(os.path.isfile('render_test_1.jpg'))

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderSceneTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()
