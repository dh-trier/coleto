# Coleto

Coleto is a collation tool for the comparison of two variant texts. It was created for the purpose of Computational Literary Studies, where texts may exist in more than one version and it is of interest to compare them. 

Coleto takes two similar but not identical versions of a text as input, identifies all passages with differences between the two versions, attempts to describe and classify each difference, and visualizes the results.

See: [Erik Ketzan and Christof Schöch, "Classifying and Contextualizing Edits in Variants with Coleto: Three Versions of Andy Weir’s *The Martian*," *Digital Humanities Quarterly* 15:4 (2021)](http://digitalhumanities.org/dhq/vol/15/4/000579/000579.html). 

This image compares two variants of Andy Weir's science fiction bestseller, *The Martian*. Here, Coleto compares Weir's original self-published version of *The Martian* (2011), and a later, professionally edited and published version (2014, Crown). Note the big spike at the far right — this indicates where an epilogue was removed from the first variant and some text inserted in the second:

![Coleto progression visualization](https://raw.githubusercontent.com/dh-trier/coleto/main/images/coleto_progression.jpg)

Coleto also generates a .tsv spreadsheet of the differences between the texts. Here, Coleto compares *The Martian* (2014) and *The Martian: Classroom Edition* (2016), which removed and replaced the novel's extensive profanity with "softer" language:

![Coleto diff table](https://raw.githubusercontent.com/dh-trier/coleto/main/images/coleto_diff_table.png)

## How to use Coleto? Documentation

Basically, the user places two .txt files into the right folder, modifies the config.yaml file to point Coleto  to the right folder and language selection (English, French, or German), and then the user runs a single command in their terminal. That's it! Coleto then generates all the visualizations and tables.

For full requirements, installation, and instructions, see [how-to](https://github.com/dh-trier/coleto/blob/main/HOWTO.md).

## Development status and roadmap 

Coleto is research software, but is actively being developed as of December 2021.

Next steps on our development roadmap: See the issues and milestones in the [repository's issue tracker](https://github.com/dh-trier/coleto/issues). 

### Version history 

* v0.1.0 (codename "Martian release"). Our first official release. DOI: [10.5281/zenodo.4569328](https://doi.org/10.5281/zenodo.4569328). 

## Context 

Coleto has been developed by Christof Schöch (Trier University, Germany) for a joint project with Erik Ketzan (University of Cologne, Germany), in which we analyzed several versions of Andy Weirs _The Martian_.
