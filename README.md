pact-plan-to-dot
================

Generate a Graphviz Dot Graph from a Stratosphere PACT Plan


## How To get JSON plan

Use the `LocalExecutor.getPlanAsJSON(Plan p)` method from Stratosphere.eu to dump your plan as JSON.


# Usage

```
Usage: 
python generate.py <json infile> <dot outfile>
```

Example
```
python generate.py plan.json plan.dot
```


