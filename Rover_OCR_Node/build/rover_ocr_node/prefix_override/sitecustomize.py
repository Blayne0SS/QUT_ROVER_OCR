import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/blayne/Rover_OCR_Node/install/rover_ocr_node'
