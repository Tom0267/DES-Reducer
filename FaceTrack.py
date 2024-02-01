import os
import glob
import dlib

faces_folder = "Resources/faces"                                                #path to the folder containing the images
training_xml_path = (faces_folder+"/training_with_face_landmarks.xml")         #path to the training xml file

if not os.path.isfile("predictor.dat"):                                         #check if the shape predictor file exists
    options = dlib.shape_predictor_training_options()                           #initialize the shape predictor training options
    options.oversampling_amount = 600                                           #increase the oversampling amount
    options.nu = 0.05                                                           #set the nu value
    options.tree_depth = 4                                                      #set the tree depth
    options.be_verbose = True                                                   #set the verbose option
    dlib.train_shape_predictor(training_xml_path, "predictor.dat", options)     #train the shape predictor
    print("\nTraining accuracy: {}".format(dlib.test_shape_predictor(training_xml_path, "predictor.dat")))      #print the training accuracy

predictor = dlib.shape_predictor("predictor.dat")               #load the pretrained shape predictor
detector = dlib.get_frontal_face_detector()                     #load the detector

win = dlib.image_window()                                       #initialize the window

for f in glob.glob(os.path.join(faces_folder, "*.jpg")):    #loop through the images in the faces folder
    print("Processing file: {}".format(f))                  #print the file name
    img = dlib.load_rgb_image(f)                            #load the image

    win.clear_overlay()                                     #clear the overlay
    win.set_image(img)                                      #set the image

    dets = detector(img, 1)                                 #detect faces in the image
    print("Number of faces detected: {}".format(len(dets))) #print the number of faces detected

    for k, d in enumerate(dets):                            #loop through the faces detected
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))        #print the coordinates of the face

        shape = predictor(img, d)                                                   #get the landmarks for the face in box d           
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))    #print the coordinates of the landmarks

        win.add_overlay(shape)  # Draw the face landmarks on the screen.

    win.add_overlay(dets)           #draw the face box on the screen
    dlib.hit_enter_to_continue()    #wait for the user to press enter