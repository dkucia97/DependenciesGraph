import unittest 
import graph as g
from unittest import TestCase, mock
import networkx.algorithms.isomorphism as iso
import networkx
import io

class Testing(unittest.TestCase):
    
    def test_extract_filename_work(self):
        filename="sample.py"
        self.assertEqual(g.extract_filename(filename),"sample")
    

    def test_get_python_files_work(self):
        with mock.patch("graph.listdir") as m:
            m.return_value=["1.py","2.py","3.txt"]
            correct_result=["1.py","2.py"]
            f=g.get_python_files("")
            self.assertEqual(f,correct_result)

    def test_get_python_files_return_empty_list(self):
        with mock.patch("graph.listdir") as m:
            m.return_value=["1.clv","2.exe","3.txt"]
            correct_result=[]
            f=g.get_python_files("")
            self.assertEqual(f,correct_result)
        
    def test_count_method_work(self):
        with mock.patch('graph.open') as m:
            #Someone know better idea for mocking file?
            m.return_value= io.StringIO("def fun() : fdfsfsdffsf \n sample text \n def metoda():fdfsd")
            correct_result=0
            f=g.count_method("","fun","metoda")
            self.assertEqual(f,correct_result)

    def test_count_method_size_return_3(self):
        with mock.patch('graph.open') as m:
            m.return_value= io.StringIO("def fun() :\n fdfsfsdffsf \n sample text \n fdsfsdfsdsdff")
            correct_result=3
            f=g.count_method_size("","fun")
            self.assertEqual(f,correct_result)

    #not pass ,bug in method / 
    def test_count_method_size_file_notcontain_method(self):
        with mock.patch('graph.open') as m:
            m.return_value= io.StringIO("def fun3() :\n fdfsfsdffsf \n sample text \n fdsfsdfsdsdff")
            correct_result=0
            f=g.count_method_size("","fun")
            self.assertEqual(f,correct_result)

    def get_expected_graph(self):
        gg=networkx.DiGraph()
        gg.add_edge("node","sample",w=1)
        gg.add_edge("node","agh",w=1)
        return gg

    def test_find_edges_in_file_work(self):
        with mock.patch('graph.open') as m:
            with mock.patch("sample.count_import") as s:
                s.return_value=1
                m.return_value= io.StringIO("import sample \n from agh")
                gg=networkx.DiGraph()
                g.find_edges_in_file("node.py",gg,"/")
                em = iso.numerical_edge_match('weight', 1)
                # equality of graph
                self.assertTrue(networkx.is_isomorphic(gg,self.get_expected_graph(), edge_match=em))

    def test_find_edges_in_file_different_weight(self):
        with mock.patch('graph.open') as m:
            with mock.patch("sample.count_import") as s:
                s.return_value=2
                m.return_value= io.StringIO("import sample \n from agh")
                gg=networkx.DiGraph()
                g.find_edges_in_file("node.py",gg,"/")
                em = iso.numerical_edge_match('weight', 1)
                # equality of graph
                self.assertFalse(networkx.is_isomorphic(gg,self.get_expected_graph(), edge_match=em))

    def test_get_functions_names_from_file_work(self):
        with mock.patch('graph.open') as m:
            m.return_value= io.StringIO("\n".join(["def fun1() ...","def metoda()v..","gfdsf"]))
            correct_result=["fun1","metoda"]
            f=g.get_functions_names_from_file("")
            self.assertEqual(f,correct_result)




   

if __name__ == '__main__':
    unittest.main()