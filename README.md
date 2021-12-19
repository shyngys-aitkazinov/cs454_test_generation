# Test Suite generation for Python

## Environment preparation

### Important: We support Only Unix-like OSes
We tested the system on MacOS, on Ubuntu also should work fine

1. Clone the repository.
2. Make a virtual environment.
```
virtualenv venv --python=python3.8
source venv/bin/activate
```
3. Install Python packages
```
pip install -r requirements.txt
```

## Limitations and precautions
Our system supports __functions, classes and  methods__. It supports the configuration of GA algorithms through the command line with following  parameters (it can run without specifying parameters that will set default parameters)..

Run this helper command to observe GA options:
```
python src/main.py -h
```

There are also several internal parameters for the testcases generation.
First, you can modify `ga_config` dictionary in ` main.py` to configure the 
test suite parameters. 
You can limit the number of statement lines in testcase (`"limit_test_lines"`), or the number of 
maximum testcases per each testsuite (`"limit_suite_testcases"`), and `random_testcase_rate` is a probability
for random testecase generation during mutation phase.
```
ga_config = {
        "pop_size": options.population_size,
        "mutation_rate": options.mutation_rate,
        "crossover_rate": options.crossover_rate,
        "module_name": (module_name, utils.relative_path_from_module_name(module_name)),
        "limit_test_lines": 10,
        "limit_suite_testcases": 4,
        "sut_info": cluster,
        "output_folder_path": output_folder_path,
        "selection": options.selection_type,
        "random_testcase_rate": 0.1
    }


```

Also, the __timeout time__ for each testcase can be configured by modifying the constructor of 
__Testcase__ class in __testcase.py__.

The guidelines for the test modules are as follows. We support functions, classes, and methods with type annotations. We also support classes as parameters for any callable things (e.g. functions, methods, etc). However we don’t support collections for our current version of the code. The module without type annotations has unpredictable behaviour. 

For testing, either code the test modules yourself, with careful examination of potentially harmful objects (file delete, disk erase, etc), or run the code in the container (e.g. docker). 
We provide some of the simple modules

## How to run the program
1. Prepare the module you want to test. (We prepared test several modules already in `examples` folder`).
2. Place your module into `examples` folder (with relevant dependencies).
3. Run the program with following command.
```
python ./src/main.py -t queue_example
```
or (with relative path)
```
python ./src/main.py -t arithmetics.complex
```
4. The final coverage will be printed and the resulted graph will be shown.
The resulted test suites will be saved in `outputs` folder. 
The testsuites are saved in decreasing order.

