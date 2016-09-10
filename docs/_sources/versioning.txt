################
qtmud Versioning
################

Versioning is an important part of making sure the progression of the code 
stays understandable over time.

qtmud uses, more or less, `semantic versioning <http://semver.org>`, modified 
to work with our :docs:`flow <flow.rst>`:

Semantic Versioning
###################

Given a version number **MAJOR**.MINOR.*PATCH*, increment the:

* **MAJOR** version when you make incompatible API changes,
* MINOR version when you are expanding the api in a backward compatible way
* *PATCH* version when you making changes to the existing api in a backward 
  compatible way.
 
Local Conventions
#################

There are a few differences from how versioning works with qtmud:

* Changes to `lib/` are only ever considered *PATCH*es. Only expansion to 
  the actual engine API should cause the MINOR version to be incremented. 
  I think this will do a better job of making it clear what version of the 
  engine is running what version of your library. Plus, if trends on other 
  game engines is any indication, many features will start in `lib/`, and 
  move over to the engine once they are well-tested. So doing this would 
  prevent the MINOR version from incrementing twice for the same code.
* Versions prior to 0.1.0 do not follow this convention. I'm considering 
  versions <0.1.0 as prototype or draft versions. Don't expect any 0.0.* 
  to have any sort of backward or forward compatibility. The API is not 
  finished, undocumented, and therefore not "released", so changes to it 
  don't justify a MINOR or **MAJOR** version bump. Otherwise, we'd be on 
  version 967.2817.3.

Application
###########

Read about :docs:`our flow <flow.rst>` to learn how to implement our versioning 
system.

Examples
########

Again, check :docs:`our flow <flow.rst>` to learn how to implement versioning.
