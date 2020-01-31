import unittest
from os import linesep
import subprocess
#from subprocess import PIPE

class Test_input_terminal(unittest.TestCase):

    def test_main(self):
        test_file = "tests/1.0_tests/teste1.txt"
        sol_file = "tests/1.0_tests/sol1.txt"
        src_file = "src/Formulos/main.py"

        output = get_program_output(test_file,src_file)

        sol = get_text(sol_file)
        sol = linesep.join([s for s in sol.splitlines() if s])

        last_space = output.rindex(" ")
        output = output[last_space:]


        self.assertEqual(int(sol), int(output))

    """
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """

def get_text(test_file):
    with open(test_file, 'r') as file:
        data = file.read()
    return data

def get_program_output(test_file,src_file):
    data = get_text(test_file)
    data = str.encode(data)
    
    output = subprocess.run(["python3",src_file],input = data,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    text = output.stdout.decode("utf-8")
    text = linesep.join([s for s in text.splitlines() if s])
    text.strip()

    return text

if __name__ == '__main__':
    unittest.main()

    """
    text = "bla \nbla"
    text = linesep.join([s for s in text.splitlines() if s])
    print(text)
    """