import os
import sys
import glob
import dlib

faces_folder = "Resources/faces"

options = dlib.shape_predictor_training_options()     
options.oversampling_amount = 300
options.nu = 0.05 
options.tree_depth = 2                                                              #depth of tree
options.be_verbose = True                                                               #prints out training progress
training_xml_path = os.path.join(faces_folder, "training_with_face_landmarks.xml")      #path to training xml file
dlib.train_shape_predictor(training_xml_path, "predictor.dat", options)                  #train the model

print("\nTraining accuracy: {}".format(dlib.test_shape_predictor(training_xml_path, "predictor.dat")))                      #prints out training accuracy

predictor = dlib.shape_predictor("predictor.dat")
detector = dlib.get_frontal_face_detector()

print("Showing detections and predictions on the images in the faces folder...")
win = dlib.image_window()
for f in glob.glob(os.path.join(faces_folder, "*.jpg")):
    print("Processing file: {}".format(f))
    img = dlib.load_rgb_image(f)

    win.clear_overlay()
    win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
        #get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),shape.part(1)))
        
        win.add_overlay(shape)      #draw the face landmarks on the screen.

    win.add_overlay(dets)
    dlib.hit_enter_to_continue()
    