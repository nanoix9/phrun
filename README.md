# Phase Running

Management and run tasks in phases

# Motivation

As a data miner or machine learner, I usually have to deal with many datasets, 
as well as many tasks such as preprocessing, feature transforming, modeling training,
predicting, and model evaluation. Each step will consume some datasets and produce
new datasets. Some steps might be time costly, such as CSV file reading and formatting,
model traing, etc. Suppose I create a pipeline with three steps: preprocess, features 
transforming, and training an logistic model. Then I made some change, say modifying
parameters, or changing to a SVM, then I just want to run the model training step instead
of the whole 3 steps.

To deal with this problem, this repo is for splitting the whole process into different phases and 
caching intermediate files so that the task could be executed in an intermediate phase instead of 
from the very beginning.

# Examples

```py
import phrun

app = phrun.App('foo')
app.get_runner() \
    .add_phase('src', lambda: (1, 2)) \
    .add_phase('add', lambda x: x[0] + x[1]) \
    .add_phase('pow', lambda x: x ** 2)
```

and run the following command

```bash
python foo.py 
```

Next time you can run it from the second, i.e., 'add' phase via 
`python foo.py -p add` or `python foo.py -i 1`

try `python foo.py -h` for more options
