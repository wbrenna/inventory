#!/bin/bash

echo "<root>" > complete_cronometer_data.xml
cat ../CRONOMETER-data/foods/*.xml >> complete_cronometer_data.xml
echo "</root>" >> complete_cronometer_data.xml
