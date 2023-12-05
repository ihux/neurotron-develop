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

* auto sizing of label in monitor
* bug: crash if 3 synapses are increased to 4
* bug: decoder not working well

# Done

* auto dimensioning of token in Cell
