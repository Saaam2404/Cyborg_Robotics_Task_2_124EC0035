from main import detect_faulty_squares
import cv2 as cv
import os

# Get the directory of the current script (test.py)
script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(script_dir, "Test_images", "faulty_chessboard_1.png")
print(file_name)

# Load the image
input_board_image = cv.imread(file_name, 1)

# Check if the image was loaded successfully
if input_board_image is None:
    print(f"Error: Could not load image at {file_name}. Check the file path and ensure the file exists.")
    exit(1)

# Call the function to detect faulty squares
output_dict = detect_faulty_squares(input_board_image)
print('Faulty_Squares: ', output_dict)

# Ground truth: (Faulty_Color, Position) => Original_Color (corrected)
faulty_chessboard_1_dict = {
    ('Red', 'A2'): 'Black',
    ('Green', 'C4'): 'Black',
    ('Red', 'D4'): 'White',
    ('Green', 'E7'): 'White',
    ('Blue', 'F4'): 'White',
    ('Blue', 'G7'): 'White',
    ('Red', 'H7'): 'Black'
}


# # TO check the test case uncomment below lines.

# # Check if the output is a dictionary
if not isinstance(output_dict, dict):
    print("Error: detect_faulty_squares must return a dictionary.")
else:
    print("\nTesting output against ground truth for faulty_chessboard_1.png...")
    passed = True

    # Check sorting (Row 1 to 8, A to H, colors: Green, Orange, Red, Blue)
    color_order = {'Green': 1, 'Orange': 2, 'Red': 3, 'Blue': 4}
    expected_keys = sorted(faulty_chessboard_1_dict.keys(), key=lambda x: (int(x[1][1]), x[1][0], color_order[x[0]]))
    output_keys = sorted(output_dict.keys(), key=lambda x: (int(x[1][1]), x[1][0], color_order.get(x[0], 5)))

    if expected_keys != output_keys:
        print("Sorting issue: Keys must be sorted by coordinates (Row 1 to 8, A to H) and colors (Green, Orange, Red, Blue).")
        print(f"Expected key order: {expected_keys}")
        print(f"Got key order: {output_keys}")
        passed = False
    else:
        # Check for missing or incorrect entries
        for key in faulty_chessboard_1_dict:
            if key not in output_dict:
                print(f"Missing key: {key}")
                passed = False
            elif output_dict[key] != faulty_chessboard_1_dict[key]:
                print(f"Mismatch for {key}: Expected {faulty_chessboard_1_dict[key]}, Got {output_dict[key]}")
                passed = False

        # Check for extra keys in output
        for key in output_dict:
            if key not in faulty_chessboard_1_dict:
                print(f"Extra key in output: {key}")
                passed = False

    if passed:
        print("Hurray! Test case Passed for faulty_chessboard_1.png.")
    else:
        print("Sorry, your Test case Failed.")

    print("\nNote: This is a sample test for one image. Run evaluator.py to test all 10 images and generate your submission file.")