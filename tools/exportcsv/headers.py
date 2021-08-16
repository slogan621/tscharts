#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import sys

lines = tuple(open(sys.argv[1], 'r'))
count = 0
ret = ""
for x in lines[1:]:
    f = x.split('\t')
    ret += f[0]
    if count < len(lines) - 2:
        ret += '__'
    count = count + 1
print(ret)
