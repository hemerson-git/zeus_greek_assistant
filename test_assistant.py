import unittest
from assistant import *

CALLING_ZEUS = "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/calling_zeus.wav"
CALLING_OTHER_NAME= "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/calling_other_name.wav"

class TestingAssistantName(unittest.TestCase):
  def setUp(self):
    start()

  def test_recognize_name(self):
    command = process_audio_command(CALLING_ZEUS)
    command = command.split()

    assistant_name = ""
    if(len(command)):
      assistant_name = command[0].lower()
      print("assistant name: {}".format(assistant_name))
    
    self.assertIn('zeus', assistant_name)
  
  def test_dont_recognize_other_name(self):
    command = process_audio_command(CALLING_OTHER_NAME)
    command = command.split()

    assistant_name = ""
    if(len(command)):
      assistant_name = command[0].lower()
      print("assistant name: {}".format(assistant_name))
    
    self.assertIn('zeus', assistant_name)

class TestingWhoIs(unittest.TestCase):
  

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = unittest.TestSuite()

    tests.addTest(loader.loadTestsFromTestCase(TestingAssistantName))

    executor = unittest.TextTestRunner()
    executor.run(tests)
