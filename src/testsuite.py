from testcase import *

class TestSuite( object ):
    def __init__(self, limit , module, sut_info):
        self.test_cluster = []
        self.limit = limit
        self.module = module
        self.sut_info = sut_info
        

    def generate_random_test_suite(self):
        for i in range( self.limit ):
            testcase = Testcase(self.module, self.sut_info.objects_under_test, 4 )
            testcase.generate_random_testcase()
            self.test_cluster.append( testcase )
        
        print( self.test_cluster )
        self.write_test_file()

        return

    def write_test_file(self):
        #writes the whole test suite into the file 
        folder_name = "testsuite_" + self.module
        folder_path = str(Path().absolute()) + '/examples'
        path = os.path.join(folder_path,folder_name)
        count = 0

        if not os.path.exists(path):
            os.mkdir(path)

        for testcase in self.test_cluster:
            test_name = "test_" + str( count ) + ".py"
            p = os.path.join( path, test_name )
            f = open( p, "w+")
            print ( testcase.statement_list )
            for statement in testcase.statement_list:   
                f.write( statement + "\n" )
            f.close()
            count += 1
    
        
        

        

