import os
import glob
import dlib

class faceDetection:

    def __init__(self):
        self.faces_folder = "Resources/faces"                                                #path to the folder containing the images
        self.training_xml_path = (faces_folder+"/training_with_face_landmarks.xml")         #path to the training xml file
        if not os.path.isfile("predictor.dat"):                                         #check if the shape predictor file exists
            options = dlib.shape_predictor_training_options()                           #initialize the shape predictor training options
            options.oversampling_amount = 600                                           #increase the oversampling amount
            options.nu = 0.05                                                           #set the nu value
            options.tree_depth = 4                                                      #set the tree depth
            options.be_verbose = True                                                   #set the verbose option
            dlib.train_shape_predictor(training_xml_path, "predictor.dat", options)     #train the shape predictor
            print("\nTraining accuracy: {}".format(dlib.test_shape_predictor(training_xml_path, "predictor.dat")))      #print the training accuracy