# To build Neurotron Package From Scratch

```
   $ cd <gitroot>   # directory containing .git folder
   $ make
```

or

```
   $ cd <gitroot>
   $ . go
   $ po -n  # poetry build/install neurotron package without testing
```

# To Update Neurotron Package

```
   $ make neurotron
```

or

```
   $ po  # poetry test/build/install neurotron package
```

# Todo's

* bug: John not correctly predicted
* bug: decoder not working well
* bug: crash if 3 synapses are increased to 4
* install at python hub

# Done

* auto dimensioning of token in Cell
* auto sizing of label in monitor
* Text() - text manager
* learning on the fly during training
* implement cells.plot
