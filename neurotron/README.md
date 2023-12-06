# Getting Started

```
Important: Be sure to have python3 / version 3.11 or higher installed
```

## To build Neurotron Package From Scratch

```
   $ cd <gitroot>   # directory containing .git folder
   $ . go           # dot-go - same as `source go`
   $ make
```

## To Update Neurotron Package

```
   $ make neurotron
```

or

```
   $ po  # poetry test/build/install neurotron package
```

## To Test Neurotron Package

```
   $ python     # start python interpreter
   >>> help(neurotron)
   Help on package neurotron:

   NAME
       neurotron

   DESCRIPTION
       neurotron: building blocks for neural computing circuits
           classes:
               Ansi        provide ANSI color sequences
               Attribute   base class to support compact attribute access
               Matrix      matrix class
               ...
```

## To Start Jupyter Lab

```
   $ jl     # start jupyter lab (same as: `jupyter lab`)
```

## To Uninstall/Reinstall Neurotron Package

```
   $ po -u  # uninstall neurotron package
   $ po -n  # reinstall neurotron package (no testing)
   $ po     # test/rebuild/reinstall neurotron (after invoking `po -n` first)
```

# Bash Environment

## To Activate Bash Environment

```
   $ cd <gitroot>   # directory containing .git folder
   $ . go           # dot-go - same as `source go`
```

Remarks:
* `. go` command must be excuted in the <gitroot> directory (where `.git` is
  located)
* the command `$ . go` sources the script `go` which sets up a couple of aliases
  which can be investigated with the `$ alias` command
* one of this alias is `?` which gives a help overview about important local
  (alias) commands to be used with `neurotron` development

```
   $ ?    # print help information (`$ bash local/bin/hlp`)
   to access local utilities
     . go          # ´dot-go´ (to access local utilities)

   help on local utilities in this repo (see alias and local/bin)
     ec            # echo colored text
     id            # launch python idle app
     jl            # launch jupyter lab
     de            # deactivate virtual environment
     ve            # activate virtual environment
     po            # poetry test/build/install

   help on standard tools
     make          # GNU make utility
     jupyter lab   # launch jupyter lab
     pip           # python package installer
     python        # launch python interpreter
     poetry        # python package manager

     try these commands with -? or --help option to get additional help
```

To see how the aliases are tied up with BASH scripts use `$ alias`:
```
   $ alias
   alias ?='bash .../local/bin/hlp'
   alias de='deactivate'
   alias ec='bash .../local/bin/ec'
   alias jl='bash .../local/bin/jl.sh'
   alias po='bash .../local/bin/po'
   ...
```

# Package Maintainance

## Todo's

* install at python hub


## Done

* auto dimensioning of token in Cell
* auto sizing of label in monitor
* Text() - text manager
* learning on the fly during training
* implement cells.plot
* bug fix: John not correctly predicted
* bug fix: decoder not working well
* bug fix: crash if 3 synapses are increased to 4
