import unittest
from assistant import *

CALLING_ZEUS = "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/calling_zeus.wav"
CALLING_OTHER_NAME= "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/calling_other_name.wav"

WHO_IS_ATHENA = "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/calling_zeus.wav"

HOW_PANDORA_BORN = "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/how_pandora_was_born.wav"

GREEK_AUTHORS = "/home/hemerson/Documents/development/IFBA/IA/assitente_mitologia_grega/audios/greek_mythology_authors.wav"

class TestingAssistantName(unittest.TestCase):
  def setUp(self):
    start()

  def test_recognize_name(self):
    command = process_audio_command(CALLING_ZEUS)
    command = command.split()

    assistant_name = ""
    if(len(command)):
      assistant_name = command[0].lower()
      print("nome do assistente: {}".format(assistant_name))
    
    self.assertIn('zeus', assistant_name)
  
  def test_dont_recognize_other_name(self):
    command = process_audio_command(CALLING_OTHER_NAME)
    command = command.split()

    assistant_name = ""
    if(len(command)):
      assistant_name = command[0].lower()
      print("nome chamado: {}".format(assistant_name))
    
    self.assertNotIn('zeus', assistant_name)

class TestingWhoIs(unittest.TestCase):
  def setUp(self):
    start()

  def test_who_is(self):
    command = process_audio_command(WHO_IS_ATHENA)
    print("comando reconhecido: {}".format(command))

    action, object = tokenize_command(command)
    is_valid = validate_command(action, object)

    self.assertTrue(is_valid)

class TestingHow(unittest.TestCase):
  def setUp(self):
    start()

  def test_who_is(self):
    command = process_audio_command(HOW_PANDORA_BORN)
    print("comando reconhecido: {}".format(command))

    action, object = tokenize_command(command)
    is_valid = validate_command(action, object)

    self.assertTrue(is_valid)
    
class TestingWhat(unittest.TestCase):
  def setUp(self):
    start()

  def test_who_is(self):
    command = process_audio_command(GREEK_AUTHORS)
    print("comando reconhecido: {}".format(command))

    action, object = tokenize_command(command)
    is_valid = validate_command(action, object)

    self.assertTrue(is_valid) 

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = unittest.TestSuite()

    tests.addTest(loader.loadTestsFromTestCase(TestingAssistantName))
    tests.addTest(loader.loadTestsFromTestCase(TestingWhoIs))
    tests.addTest(loader.loadTestsFromTestCase(TestingHow))
    tests.addTest(loader.loadTestsFromTestCase(TestingWhat))

    executor = unittest.TextTestRunner()
    executor.run(tests)
