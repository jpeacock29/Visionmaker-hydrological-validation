---
title: Validation of the Visionmaker NYC Hydrological Model
author:
- Jacob Peacock
- Katie Smith
- Maya Kutz
- New York City Engineers for a Sustainable World
date: \today{}
abstract: Visionmaker NYC is a web-based, user-friendly environmental modeling system for New York City (NYC) created by the Wildlife Conservation Society (WCS). We empirically evaluate the floodwater component of the hydrological model contained within Visionmaker against observed flooding using reports from the NYC 311 help phone line and historical precipitation data. Of the 26 flood events identified from 2015, we tested 10 in Visionmaker and found that in no cases did Visonmaker NYC predict flooding correctly. The simplified "bucket model" for precipitation and drainage used by Visionmaker is the likely cause of this disparity and the hydrological model should be adjusted to include time dependence. We also critically evaluate the storm models used by Visionmaker and find significant disparities with other climatic data that should be addressed.
toc: true
---

\newpage{}

Introduction
============
Visionmaker NYC[^1] is a web-based, user-friendly environmental modeling
system for New York City (NYC) created by the Wildlife Conservation
Society (WCS). To build a model, the user chooses parameters like
climate scenario, precipitation events, and land-use types, collectively
referred to as a “Vision” for the city. The model then predicts water usage,
biodiversity, greenhouse gas emission,
sustainable population, and other outputs for a selected area of NYC.
Using this simplistic model, the user can gain a better understanding
and appreciation for the dynamics and environment of the city.

Visionmaker is still in development, and many of the models which
predict metrics of sustainability have not been validated. Starting in
the Spring of 2016, we volunteered through Engineers for a Sustainable
World NYC (ESW-NYC) to assess Visionmaker’s hydrological model. The model and
the variables it relates are shown in Figure 1.[^2]

<center>

![Visionmaker models hydrology in NYC as a simple flow-through
bucket model: different components contribute to water input into the
city’s geography (“ecosystem type” in Visionmaker), which ultimately
determines the amount of runoff.](flowchart.jpg)

</center>

In a “black box” approach to validation, we evaluated the models prediction
of street flooding (“Undifferentiated Floodwaters” in Visionmaker) against
actual resident reports of flooding during rain storms. We also evaluated the
modeling of rain storms within Visionmaker and compared this model with
observed and projected rainfalls published by the Northeast Regional
Climate Center (NRCC).

Throughout this report, file names will be referenced as
`file/name/here.txt` and the corresponding files can be found hosted on
Github.[^3]


Testing Flood Predictions
=========================
Here, we empirically evaluate the floodwater component of the
hydrological model contained within Visionmaker against observed
flooding. Using reports from the NYC 311 help phone line, where
residents frequently call to report hazardous or bothersome conditions
and request services from the city, we generate a conservative estimate
of when and where in NYC flooding occurred in 2015. Daily historical
weather data was used to estimate the quantity of precipitation
ostensibly causing each flood. This precipitation was then modeled in
Visionmaker, producing a predicted volume of flood water. Comparing
whether Visionmaker predictions of flooding coincide with known
incidences of flooding allows us to test the efficacy of the model.


Methods
-------

### Mining 311 data for flooding events
Data on 311 reports from 2015 was obtained from the NYC Open Data
portal.[^4] Using the python programming language, the reports were
filtered for those with (1) the word “flood” in the “Descriptor” field,
(2) a “Complaint Type” of “Sewer” and (3) a provided longitude and
latitude. Of the \~2.3 million reports, 9189 fitting this criteria were
found.

From these 9189 reports of flooding, we identified "storm periods" as
consecutive days of the year with more than 50 reports of flooding. This
threshold was chosen heuristically to include most of the peaks observed
in Figure 2. For each of these 19 storm periods, we identified
geospatial clusters of flooding reports where several reports of
flooding were made in close geographic proximity. We applied the DBSCAN
algorithm to perform the clustering using the longitudes and latitudes
given in the flood reports. We represent each cluster as a single “flood
event” occurring at the average time and location of the flood reports
composing the cluster.

<center>

![The number of reports of flooding on each day of the year. The
dashed horizontal line indicates our cut-off threshold for a "storm
period".](../outputs/flood_reports.png)

</center>

This analysis can be reproduced by running `make.sh`. Note that the
DBSCAN algorithm is non-deterministic and may not produce exactly the
same results in each run.


### Details of the DBSCAN algorithm
The DBSCAN algorithm requires two parameters: $n$, the number of reports
required to form a cluster, and $\epsilon$ which, roughly, indicates the
maximum distance allowed between reports in the same cluster. We choose
these parameters conservatively, erring on the side of caution in order
to select only the most likely flooding events. Thus, we required
$n = 3$ reports of flooding to form a cluster and $\epsilon$
corresponding to approximately 0.25 miles as the maximum distance
between reports in a cluster. The clusters include only those reports
that appeared close together; many others are classified as “outlier”
points by the DBSCAN algorithm and ignored in further analysis.

Lastly, we note that the clustering algorithm applied Euclidean distance
to the longitudes and latitudes of the reports and imparts a slight
distortion. (Specifically, while 1 degree of latitude is 69 statutory
miles, 1 degree of longitude is \~53 statutory miles at the latitude of
NYC. Thus reports separated by 1 degree of longitude are actually closer
together than those separated by 1 degree of latitude; however, the
algorithm would treat the points as the same distance apart.) Since we
are dealing with a relatively small area far from the poles, this
distortion likely negligibly affects the results of the clustering and
our later analysis. To correct this, we might use the Vincenty distance
during clustering.

### Cross-referencing daily precipitation

Daily precipitation data was obtained from the Northeast Regional
Climate Center using the Central Park weather station.[^5] Precipitation
is given in inches of rainfall and liquid equivalent of snowfall. For
each of the flooding events identified in the 311 data, we summed the
reported precipitation for each day spanned by the flood event (column
`central_park_daily_precipitation_inches` of
`Visionmaker_modelling_results/Visionmaker_flood_predictions.csv`).

### Modeling in Visionmaker

For each flooding event, the aggregated precipitation was used to model
the flooded area in Visionmaker as follows, making reference to the columns of the
spreadsheet
`Visionmaker_modelling_results/Visionmaker_flood_predictions.csv`:

1.  After opening Visionmaker and logging in, follow the menus and
    buttons: `Manage > Visions > Create New Vision`. Visions were named
    as `test_` followed by the identifier from column `flood_id`. No
    additional parameters were set and the default “Base on” value of
    “New York City (2014)” was retained.

2.  Since the flooding events are marked by longitude and latitude, but
    Visionmaker does not provide a search functionality for
    longitude and latitude, Google Maps was used to assist in locating
    flooding events. Once zoomed to the appropriate level (ie, 17), the
    geographic area of the Vision is defined as the blocks surrounding
    the specified longitude and latitude and the Vision is saved.[^6]

3.  The aggregated precipitation of the flooding event is next converted
    to the appropriate Visionmaker parameters. Internally, the
    Visionmaker model uses the product of two parameters, storm
    duration and storm intensity, to determine the total precipitation
    of a storm. Since Visionmaker uses a “bucket model” in
    determining floodwater output, only this total precipitation affects
    the results.[^7] Externally, these two parameters are determined by
    two broader parameters, “Climate” and “Rain Event”. The Visionmaker
    NYC parameters used for each flood event and the total precipitation
    are found in columns `visionmaker_precipitation_event`,
    `visionmaker_climate` and
    `visionmaker_total_precipitation`, respectively. These values were
    selected with the aide of a table relating each combination of
    “Climate” and “Rain Event” to the corresponding total
    precipitation[^8] and chosen to follow the observed precipitation as
    closely as possible.

4.  After inputting the appropriate values for the “Climate” and “Rain
    Event”, looking in “Environmental Performance” section “Water”, the
    value “Floodwater” is selected from the drop-down menu. The
    displayed value is reported in column `visionmaker_floodwater`.

Results & Discussion
--------------------

<center>

![The 26 flood events, red, plotted over all flood reports, blue.
Note the outline of New York City formed by the flood reports as well as the darker red points where two flood events coincide.](../outputs/flood_events_and_reports_by_location.png)

</center>

Using the 311 data, 26 flood events were identified.[^9] As a sanity
check, we observe that almost all flood events identified occurred
during periods of significant precipitation in the historical weather
record. Furthermore, flood events often overlap geographically (Figure
3), having flooded during multiple storm events, as might be expected of
a low-lying area prone to flooding. To further validate our flood
events, future work might also consider elevation data, that may
confirm flooding occurs in low-lying areas. These checks give
us some assurance that our identified flood events are plausible.

Of the 26 flood events, we modeled a sample of 10 in Visionmaker,
specifically choosing those with the highest precipitation. The
Visionmaker model did not predict flooding at any of the flood
events under the observed precipitation conditions.[^10] It is possible
that some floods occur through mechanisms outside the Visionmaker model,
like trash clogging a drainway, a pipe burst or storm surge. However, we
would expect these first two effects to account for only a fraction of
floods and storm surge would be limited to those flood events near the
coasts. The data does not substantiate any of these hypotheses and we
would nonetheless expect at least some of the flood events to correspond
to genuine precipitation-induced flooding.

The model itself seems the most likely source of failure. In particular,
Visionmaker uses a "bucket model" to calculate floodwaters: whatever
volume of the total precipitation does not runoff into streams or
stormwater drainage is accounted for as floodwaters. Under this model,
flooding only occurs when the total precipitation exceeds the volume of
stormwater and stream drainage. However, actual flooding is observed as
a transient phenomena, occurring only during brief periods of intense
precipitation. (The generally brief durations of reported floods support
this notion.) While the total volume of an intense rain event may not be
enough to overwhelm the total volume of drainage available, the *rate*
of precipitation may exceed the rate of drainage, thus producing
flooding. Since the rates of precipitation are not considered in the
bucket model, this effect may account for the disagreement between
prediction and observation.

Suggestions
-----------
-   Adjust the hydrological model to include time dependence, for
    example, by considering a precipitation rate exceeding the drainage
    rate as a cause of temporary flooding.

-   Use the data generated in this report as calibration when adjusting
    parameters and evaluating model choices.

-   Consider renaming "floodwaters" to "other runoff", since it does not
    correspond to the common understanding of a flood.

Minor:

-   Allow more precise or direct manipulation of total rainfall in
    storm events. The actual total rainfall has significant
    discontinuities; see[^8].

-   Allow search of Visionmaker by longitude and latitude.

Comparing Rainfall Data
=======================
In this section, we compare the storm parameters used in Visionmaker’s
storm events with those independently produced by the Northeast Regional
Climate Center (NRCC). In particular, we compare empirical storm
intensity models as well as predicted increases in storm intensity due
to climate change given by both sources.

Methods
-------
Visionmaker uses six storm types parameterized by intensity, duration,
and return period (equivalent to storm frequency; see Table 1).
Intensity is the rate of precipitation during a storm event in
inches per hour. Duration is how long the storm event lasts in hours. Return
period is a measure of how likely a storm is to occur. For example, a
storm with a 5-year return period has a 1/5 = 20% chance of occurring in
any given year and occurs on average once every five years.

Table 1: Six Visionmaker storm types and the baseline intensity used to
determine future intensities.

  **Rain Event**   **Duration** (hour)   **Baseline Intensity** (inch/hour)   **Return Period** (year)
  ---------------- --------------------- ------------------------------------ --------------------------
  Clear Day        0                     NA                                   NA
  Rainy Day        6                     0.65                                 2
  Severe Storm     24                    1.1                                  100
  Showers          2                     0.4                                  NA
  Soaking Storm    12                    0.6                                  10
  Thunderstorm     1                     1.75                                 5

The parameters of four of the six Visionmaker storm types are derived
from the intensity-duration-frequency (IDF) curve shown in Figure 4.
As for the other two storm types, “Clear Day” has zero rainfall and does not
require analysis, and “Showers” was not derived empirically but as an
*ad hoc* estimation.

<center>

![This IDF curve was published in a climate change impact report
by the DEP of NYC in 2008. From left to right, the red stars correspond to
“Thunderstorm,” “Rainy Day,” “Soaking Storm,” and “Severe Storm” rain
events.[^11]](idf_curve.png)

</center>

To forecast rain intensities for future climate scenarios, the same baseline
data is used, but scaled up by fixed percentages published by the NYC Panel
on Climate Change (NPCC). These percentage scaling factors describe
increases in total annual rainfall and generally result in increasing
intensity over time. The report cited for the 2100--2109 projections has
a lower scaling factor than those used for earlier projections.[^12]

To collect the NRCC data, each Visionmaker storm type was matched by
duration and return period with the interactive IDF curve published by
the NRCC for the Central Park weather station (“CNTRL PK TWR”).[^13]
This IDF curve provides projected mean rainfall intensities for
2010--2039, 2040--2069, and 2070--2099. We selected the “High RCP 8.5”
emission scenario, rather than the “Low RCP 4.5,”[^14] as it more
closely matched the Visionmaker data.

For both the Visionmaker and NRCC data, total rainfall was calculated as
the product of intensity and duration. Plots of intensity and total
rainfall were produced in R.


Results & Discussion
--------------------

<center>

![Plots of storm intensity and rainfall across different time
periods and storm types. NRCC data is shown in black; Visionmaker in
red.](../outputs/storm_parameters.png)

</center>

The NRCC and Visionmaker datasets broadly correlate, with short storms modeled
as more intense and longer storms as less intense. However, the
magnitudes of rainfall intensities are generally much higher in
Visionmaker than in the NRCC data, except for “Thunderstorms” (Figure
5). The implausibly high rainfalls of the Severe Storm far exceed
reasonable maximums and would account for most of New York City’s
average annual rainfall. The reason for this discrepancy is obscure, but
the cited IDF curve uses very old data, outdated IDF models, and the log
scale appears erroneous.[^15]

As noted in the methods, Visionmaker calculates future and past climate
scenarios using fixed percentages of the baseline intensities from the Figure 4
IDF curve. For example, 2080--2089 storm intensities are modeled as 110%
of the 1903--1950 baseline.[^16] These percentages are derived from the
total annual precipitation predictions published in various NPCC
reports. The projected future rainfall in Visionmaker roughly match the
increases in the NRCC data: both show an increase in storm intensity of
between 0.05 and 0.1 inches/hour over the 21^st^ century for all storm
types. However, the fixed percentages in the NPCC reports
are meant to represent changes to average total annual precipitation, rather
than the intensity of an individual storm. Furthermore, Visionmaker is currently set
to model everything on June 1^st^, meaning that snow and other annual variations
 (eg, seasons) should not count towards Visionmaker’s calculations.

We also noted that Visionmaker’s 2100s projections have lower
intensities and total rainfalls than the 2080s, due to a change in the NPCC
report used for these predictions. This conclusion is inconsistent with
trends of the NRCC data and likely attributable to the alternate model used.

Finally, Visionmaker uses 1609, the year the Dutch began exploring NYC for
settlement, as a Past Climate Scenario. Based on evidence showing
extreme drought in Jamestown, Virginia in 1609, Visionmaker decreased
the 1903--1950 baseline intensity by 10%. As it is not obvious that a drought in
 Virginia would reach New York, this projection needs more substantial evidence.
 Further, an intensity decline of 10% may not be consistent with observed
 extreme drought [^17].


Suggestions
-----------
-   Critically examine discrepancy between Visionmaker’s storm event
    parameters and those of the NRCC.
-   If the Figure 4 IDF curve is retained, update “baseline” time period from
    “1970--1999” to “1903--1950” to more accurately reflect source data.
-   Choose a return period and data source for the 2-hour storm type “Shower.”
-   Provide a more nuanced view of storm events and effects of
    climate change.
-   Use a single source to predict future climate scenarios.
-   Produce a more rigorous estimate of 1600s precipitation.
-   Consider showing flood map delineations, even as a simple layer
    added for different Climate Scenarios.


[^1]: <https://visionmaker.us/nyc/>

[^2]: <https://visionmaker.us/resources/models/water/>

[^3]: <https://github.com/jpeacock29/Visionmaker-hydrological-validation>

[^4]: <https://data.cityofnewyork.us/dataset/311-Service-Requests-From-2015/57g5-etyj>

[^5]: <http://climodtest.nrcc.cornell.edu/>

[^6]: Access to the "ESW-NYC" account, which contains the exact regions
    used for each model, is available upon request.

[^7]: <https://visionmaker.us/resources/models/water/'> and
    <https://visionmaker.us/info/metric/27/>

[^8]: `inputs/storm_modelling.csv`

[^9]: `outputs/311_2015_floods.csv`

[^10]: `Visionmaker_flood_predictions.csv`

[^11]: *The NYC DEP Climate Change Program Assessment and Action Plan.*
    A Report Based on the Ongoing Work of the DEP Climate Change Task
    Force; May 2008.
    <http://www.nyc.gov/html/dep/html/news/climate_change_report_05-08.shtml>

[^12]: Visionmaker uses the following sources for different time periods
    (“Climate Scenarios”):

    > 1609: Stahle et al. 1998 The Lost Colony and Jamestown droughts.
    > *Science*, New Series, Vol 280.
    > <http://www.uark.edu/misc/dendro/PUBS/1998_Science.pdf> (March 11,
    > 2017).
    >
    > 1970-2010: City of New York Department of Environmental
    > Protection. 2008. *The NYC DEP Climate Change Program Assessment
    > and Action Plan*. New York: Department of Environmental
    > Protection. <http://www.nyc.gov/html/dep/pdf/climate/climate_chapter2.pdf> (November
    > 11, 2013).
    >
    > 2020-2029 & 2050-2059: New York City Panel on Climate Change.
    > 2013. Climate Risk Information 2013:  *Observations, Climate
    > Change, Projections, and Maps*. New York: City of New York Special
    > Initiative on Rebuilding and
    > Resiliancy. <http://www.nyc.gov/html/planyc2030/downloads/pdf/npcc_climate_risk_information_2013_report.pdf> (September
    > 25, 2013).
    >
    > 2080-2089: Horton, R., O’Grady, M., & New York City Panel on
    > Climate Change. (2009). *Climate Risk Information:  New York City
    > Panel on Climate Change*. New York: New York City Panel on Climate
    > Change.
    >
    > 2100-2109: Rosenzweig, C., Solecki, W., Blake, R. A., Bowman, M.
    > J., Gornitz, V., Jacob, K. H., ..., Yohe, G. W. (2015). Appendix I:
    > Climate Risk and Projections NPCC 2015 Infographics. *Annals of
    > the New York Academy of Sciences*, 1336(1), 109--115.
    > https://doi.org/[10.1111/nyas.12715](http://dx.doi.org/10.1111/nyas.12715)

[^13]: <http://ny-idf-projections.nrcc.cornell.edu/index.html>

[^14]: This emission scenario corresponds to the higher model of
    greenhouse gas concentration given by the Intergovernmental Panel on
    Climate Change: 1200 ppm of $\rm CO_2$ equivalent by 2100, or four times
    the current concentration.

[^15]: Typically, log scales are divided into five or ten minor
    increments. This IDF curve divides into six and seven minor
    increments for the 0.1--1 and 1--10 major increments, respectively.

[^16]: Visionmaker refers to the baseline data as representing
    1970--2000, but the cited IDF curve actually uses data from
    1903--1950.

[^17]: "USGS WaterWatch -- Streamflow Conditions." *USGS WaterWatch --
    Streamflow Conditions*. 28 Mar 2017.
    <https://waterwatch.usgs.gov/?id=ww_drought>
