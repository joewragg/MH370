An Exercise in Inference: Finding a Missing Airliner
================
Author: Joe Wragg











\centerline{Project Members: Joe Wragg and Stefan Harban} 
\centerline{Project Supervisor: Professor Andrew Blain}

# Abstract

Malaysia Airlines Flight 370 (MH370) was a scheduled international
passenger flight that disappeared on the 8 of March 2014 while flying
from Kuala Lumpur Airport, to Beijing. The aircraft has not been
recovered, and the cause of the disappearance remains unknown.

# Introduction

Malaysia Airlines Flight 370 (MH370) was a scheduled international
passenger flight that disappeared on the 8 of March 2014 while flying
from Kuala Lumpur International Airport to Beijing Capital International
Airport in China. The aircraft has not been recovered, and the cause of
the disappearance remains unknown. It remains the most expensive search
and became the biggest mystery in aviation history

Analysis of satellite communications between the aircraft and Inmarsat’s
satellite communications network concluded that the flight continued
until at least 08:19 and flew south into the southern Indian Ocean,
although the precise location cannot be determined. From October 2014 to
January 2017, a comprehensive survey of 120,000 km (46,000 sq mi) of sea
floor south-west of Perth, Western Australia, yielded no evidence of the
aircraft. In January 2018, a second search has been announced to be
conducted by a searching vessel provided by private U.S. marine company
Ocean Infinity.

In a previous search attempt, Malaysia had established a Joint
Investigation Team to investigate the incident, working with foreign
aviation authorities and experts. Malaysia released a final report on
Flight 370 in October 2017.

The analysis of communications between the flight and Inmarsat’s
satellite telecommunication network provide the only source of
information about the flight’s location and possible in-flight events
after it disappeared from radar coverage at 2:22am.

The main objective of our investigation was to replicate inmarsat’s
analasis of the satelite communications and attempt to make our own
conclusions. To see if they agree with the established findings given in
the report published in october 2017.

\newpage

# Method

## Initial Path

Our first task was to attempt to find information about the plane’s
whereabouts before its dissaperrance from miliatry radar. From there we
have a starting point to then analyse the satelite data. Here is what
know from the report:

  - Malaysia Airlines Flight 370 departed Kuala Lumpur International
    Airport at 16:41 UTC on the 7th March 2014.
  - The final automatically transmitted position (ACARS) from the
    aircraft occurred at 17:07
  - No radio communications were received from the crew after 17:19
  - ACARS reports from the flight, giving heading and speed, were
    expected at 17:37 and 18:07 but were never received.
  - At 17:21, the aircraft disappeared from the radar of air traffic
    control in the South China Sea between Malaysia and Vietnam.
  - The aircraft continued to be tracked by Malaysian military radar
  - At 1725 the aircraft deviated from the flight-planned route turning
    around and crossing the Malay Peninsula.
  - Flight 370 left the range of Malaysian military radar at 18:22 and
    was last located 370 km northwest of Penang.

Here is the path predicted in the ATSB “Underwater search areas” report:

\begin{figure}[]
\centering
\includegraphics[width=\textwidth]{wide.png}
\caption{MH370 flight path derived from primary and secondary radar data}
\end{figure}

\clearpage

Unfortunately little information is given in the report. The table below
shows what information is given in the report and what is needed to be
calculated.

\begin{table}[h]
\centering
\label{my-label}
\caption{Table of path variables}
\begin{tabular}{|l|l|l|l|l|}
\hline
\textbf{Location}           & \textbf{Tiime(UTC)} & \textbf{Latitude}   & \textbf{Longitude}  & \textbf{Bearing (deg)} \\ \hline
KIA                         & TakeOff             & 2.7                 & 101.7               &                        \\ \hline
Last ACARS                  & 17:06:43            & 5.27                & 102.79              & \textit{\textbf{A}}    \\ \hline
Last Radar Contact          & 17:21:13            & \textit{\textbf{X}} & \textit{\textbf{Y}} &                        \\ \hline
Telephone Contact           & 17:52:27            & 5.2                 & 100.2               &                        \\ \hline
Last Military Radar Contact & 18:22:12            & 6.65                & 96.34               &                        \\ \hline
\end{tabular}
\end{table}

\begin{minipage}{.55\textwidth}
The bearing A is calculated in the code by taking the line between the last ACARS position and the KIA position. Then the lat, lon and bearing at last ACARS along with the time difference between last radar and last acars. Can be used to estimate X and Y. Assuming a constant speed of 450 knots.

\medskip
The latitude and longitude of the airport can be calculated from the xyz given in the report. These values are in an earth fixed coordinate system and can be converted into latitude and longitude points in the code. 

\medskip
See appendix figure \ref{table1} 
\end{minipage}
\hspace{.05\textwidth}
\begin{minipage}{.4\textwidth}
\centering
\includegraphics[width=\textwidth]{bearing.png}
\captionof{figure}{Figure Showing bearing A 25 degrees}
\end{minipage}

\pagebreak

\begin{figure}[h]

\centering
\includegraphics[width=\textwidth]{InitialPath.PNG}
\caption{Google earth preview of initial path}
\end{figure}

Once we plotted this in google earth you can see the result in the image
below: 

## BTO Analysis

The analysis of communications between the flight and Inmarsat’s
satellite telecommunication network provide the only source of
information about Flight 370’s location and possible in-flight events
after it disappeared from radar coverage at 2:22am.

\begin{table}[h]
\centering
\label{my-label}
\caption{Table showing the seven handshakes}
\begin{tabular}{lllll}
\textbf{Time (MYT)} & \textbf{Time (UTC)} & \textbf{Initiated by} & \textbf{Name (if any)}      & \textbf{Details}                                                                                                           \\
2:25:27             & 18:25:27            & Aircraft              & 1st handshake               & A 'log-on request' message. \\
3:41:00             & 19:41:00            & Ground station        & 2nd handshake               & Normal handshake                                                                                                           \\
4:41:02             & 20:41:02            & Ground station        & 3rd handshake               & Normal handshake                                                                                                           \\
5:41:24             & 21:41:24            & Ground station        & 4th handshake               & Normal handshake                                                                                                           \\
6:41:19             & 22:41:19            & Ground station        & 5th handshake               & Normal handshake                                                                                                           \\
8:10:58             & 0:10:58             & Ground station        & 6th handshake               & Normal handshake                                                                                                           \\
8:19:29             & 0:19:29             & Aircraft              & 7th handshake               & A 'log-on request' from the aircraft\\
\end{tabular}
\end{table}

\begin{minipage}{.55\textwidth}
The burst timing offset (BTO) is the time difference between the start of the time slot and the start of the transmission recieved from the aircraft. The time it takes for the signal to traverse the following: 
\begin{itemize}
\item Ground station's signal to satelite
\item Satelite to Aircraft
\item Aircraft's response back to satelite 
\item Time it takes for the aircrafts SDU(onboard computer) to respond called the SDU bias
\item Responce recieved at the ground station
\item The delay between the time the signal arrives at the ground station and the time it is processed to be sent back 
\end{itemize}
\end{minipage}
\hspace{.05\textwidth}
\begin{minipage}{.4\textwidth}
\centering
\includegraphics[width=\textwidth]{BTOFig1.pdf}
\captionof{figure}{BTO illustration}
\end{minipage}

An equation can therefore be constructed using an average distance where
\(Distance = Speed \times Time\):
\[Range(SATToAircraft) = \frac{c.(BTO-Bias)}{2} - Range(SatToGES)\]
\(Bias\) is the SDU bias and is constant for the flight and so can be
calculated using the first half an hour of flight before takeoff. Where
the aircraft’s location is fixed. \(c\) is the speed of light.
\[Bias = BTO-\frac{2[Range(SatToAircraft)-Range(SatToGES)]}{c}\] We
calculated a mean bias of -0.4950348991s, the bias ATSB uses (given in
the report is -0.495679s. See appendix figure 

We are provided with a table of times and BTO values. See appendix
figure . We can use these values to generate a list of
\(Range(SatToAircraft)\) values and times. To solve this we need a table
of times and satelite positions see computational details. Once we have
these we can then work out the distance between the satelite and the GES
which is in a constant position giving \(Range(SatToGES)\).
\[Range(SatToGES) = \sqrt{(x_{Sat}-x_{GES})^2+(y_{Sat}-y_{GES})^2+(z_{Sat}-z_{GES})^2}\]

Then finally use the first equation and both these tables to generate a
table of range values, the dist column, one for each of the seven
handshakes:

| Date                    | DateSat                 |        x |        vx |     Dist |
| :---------------------- | :---------------------- | -------: | --------: | -------: |
| 2014-03-07 18:25:27.421 | 2014-03-07 18:25:27.400 | 18136.79 | 0.0018860 | 36905.35 |
| 2014-03-07 19:41:02.906 | 2014-03-07 19:41:02.900 | 18145.32 | 0.0019099 | 36745.42 |
| 2014-03-07 20:41:04.904 | 2014-03-07 20:41:04.900 | 18152.42 | 0.0020370 | 36785.74 |
| 2014-03-07 21:41:26.905 | 2014-03-07 21:41:26.900 | 18160.03 | 0.0021580 | 36954.46 |
| 2014-03-07 22:41:21.906 | 2014-03-07 22:41:21.900 | 18167.82 | 0.0021375 | 37238.41 |
| 2014-03-08 00:10:59.928 | 2014-03-08 00:10:59.900 | 18178.16 | 0.0015841 | 37803.64 |
| 2014-03-08 00:19:29.416 | 2014-03-08 00:19:29.400 | 18178.94 | 0.0014917 | 37861.91 |

Seven handshake data, some columns excluded to fit

Appendix figure  shows an example from ATSB of how this should look for
the first half an hour of flight.

Taking a row of the table giving you a time, position of the satelite
and the range you can draw a great circle on the earth:

\begin{figure}[h]
\centering
\includegraphics{range.png}
\caption{RangeSatToAircraft and great circle}
\end{figure}

Repeating this for the seven handhshakes gives you seven arcs:

\begin{minipage}{.5\textwidth}
\centering
\includegraphics[width=\textwidth]{arcs2.png}
\captionof{figure}{Our Arcs}
\end{minipage}
\begin{minipage}{.5\textwidth}
\centering
\includegraphics[width=\textwidth]{arcs.png}
\captionof{figure}{The seven arcs from ATSB}
\end{minipage}

## BFO Analysis

An analysis of the burst frequency offset (BFO) values provided by
inmarsat (see appendix fig’ ) can determine where along the BTO arcs the
aircraft was located. The burst frequency offset is defined as the
difference between the expected and received frequency of transmissions
caused by doppler shifts.

\begin{figure}[h]
\includegraphics{BTOFig.png}
\caption{BTO illustration}
\end{figure}

  - \(\delta f_{AFC}+\delta f_{sat}\) are provided by ATSB see appendix
    figure 
  - \(\delta f_{bias}\) is provided as 152.5\(H_z\) see appendix figure 
  - This leaves \(\delta f_{down}\), \(\delta f_{up}\) and
    \(\delta f_{comp}\) to be calculated

### \(\Delta F_{down}\) calculation

Using a basic doppler shift formula with a stationary observer (GES) and
a source moving towards the observer. This direction is arbitary and
affects the sign on the bottom of the equation.
\[\Delta F_{down} = f_{down} (\frac{c}{c-v_s} -1)\]

  - where \(v_s\) is the velocity of the satelite towards the GES
  - where c is the speed of light
  - \(f_{down}\) is a constant provided by ATSB and is the frequency
    before shift of the downlink signal \(f_{down} = 3615.1525MH_z\)

We have the velocity of the satelite as an xyz vector earth fixed
geomertry. To turn this into velocity towards GES we use the vector
projection in the direction of GES
\[\textbf{v}_s = \frac{\textbf{v}\cdot \textbf{s}}{|s|}\]

\begin{minipage}{0.7\textwidth}
We need three vectors:
\begin{itemize}
\item $\textbf{v}$ is the velocity vector of the satelite given in figure \ref{data}
\item $\textbf{s}$ is the displacement vector between the satelite and the GES
$$\textbf{s}=(x_{sat}-x_{GES}, y_{sat}-y_{GES}, z_{sat}-z_{GES})$$
\item $|s|$ is the magnitude of that vector
\end{itemize}
\end{minipage}
\begin{minipage}{.3\textwidth}
\includegraphics{FDown.png}
\end{minipage}

### \(\Delta F_{up}\) calculation

Using a basic doppler shift formula with a moving observer (MH370) and
source. Both moving towards each other.
\[\Delta F_{up} = f_{up} (\frac{c+v_{s}}{c-v_{pl}} -1)\]

  - where \(v_s\) is the velocity of the satelite towards the plane
  - where c is the speed of light
  - \(f_{up}\) is a constant provided by ATSB and is the frequency
    before shift of the uplink signal \(f_{up} = 1646.6525MH_z\)

Again we have the velocity of the satelite as an xyz vector earth fixed
geomertry. To turn this into velocity towards the plane we use the
vector projection in the direction of the plane.
\[\textbf{v}_s = \frac{\textbf{v}\cdot \textbf{s}}{|s|}\]

\begin{minipage}{0.7\textwidth}
We need three vectors:
\begin{itemize}
\item $\textbf{v}$ is the velocity vector of the satelite given in figure \ref{data}
\item $\textbf{s}$ is the displacement vector between the satelite and the plane
$$\textbf{s}=(x_{sat}-x_{pl}, y_{sat}-y_{pl}, z_{sat}-z_{pl})$$
\item $|s|$ is the magnitude of that vector
\end{itemize}
\end{minipage}
\begin{minipage}{.3\textwidth}
\includegraphics{FUp.png}
\end{minipage}

### \(\delta f_{comp}\) calculation

\(\delta f_{comp}\) is defined as the frequency compensation applied by
the aircraft, to attempt to compensate for the doppler shifts. This
assumes that the satelite is in a fixed position above the equater at
its nominal position. However due to the satelite drift at the time the
delta f comp could not fully compensate for the doppler shift which is
why we see a \(\delta f{up}\) value.

The nominal position is stated in the report as a longitude of
64.5\(^{\circ}\). Above the equater therefore a latitude of
0\(^{\circ}\). There is no nominal value for the altitude given so we
would have to assume a value for this. One method could be to assume an
average value of the altitude over time.

It is also not stated in the report how this calculation is done by the
aircraft’s onboard computer. However you could assume it uses a standard
doppler shift formula assuming a stationary observer
(satelite):

\[\delta f_{comp} = f_{up} (\frac{c}{c-v_{pl}})\]

\[BFO = \Delta F_{up} + \Delta F_{down} + \delta f_{comp} + (\delta f_{AFC} + + \delta f_{sat}) + \delta f_{bias}\]

\[BFO = f_{up} (\frac{c+v_{s}}{c-v_{pl}} -1) + f_{down} (\frac{c}{c-v_s} -1) + f_{up} (\frac{c}{c-v_{pl}}) + const \]
where \(const = \delta f_{AFC}+\delta f_{sat} + \delta f_{bias}\) ;
\(v_s = |\textbf{v}_s|\) and
\(\textbf{v}_s = \frac{\textbf{v}\cdot \textbf{s}}{|s|}\)

As you can see you have two unknowns the velocity of the plane and its
position. So the only way to solve this would be to use a monte carlo or
numerical method. Finding the most probable positions and velocities
using a probabilistic analaysis along each arc for each arc.

## Finding a suitable path for the plane

We know that the plane must cross the first arc at 18:25, we also know
that it’s last known position from our initial path is the last radar
contact at 18:22.

\begin{minipage}{0.75\textwidth}
An iterative process is used to determine the path from the last radar point and the arc. This is described in more detail after this. However with our current 1st arc position the plane can not make to the arc in time. Even if it flies at the maximum theoretical speed. We discovered however that by changing our bias to the bias given in the ATSB report the arcs shift to the right towards the radar point. We also had to increase the speed for it to reach to 320$ms^{-1}$ WHY THIS SPEED. You can see the result to the right. You can also see below that the new arcs are closer to the ones provided by ATSB.

\end{minipage}
\begin{minipage}{0.2\textwidth}
\includegraphics{SprintPath.png}
\end{minipage}

\begin{minipage}{.5\textwidth}
\centering
\includegraphics[width=\textwidth]{arcs1.png}
\captionof{figure}{Our new arcs}
\end{minipage}
\begin{minipage}{.5\textwidth}
\centering
\includegraphics[width=\textwidth]{arcs.png}
\captionof{figure}{The seven arcs from ATSB}
\end{minipage}

Now we needed to find a path between each arc. Starting with the point
at 18:25. With an incomplete BFO analysis you have to make some
reasonable assumptions about the flight path:

  - Constant speed of 450 knots
  - Constant altitude of 35,000 feet
  - The plane always travels in straight lines between each arc

\begin{minipage}{0.45\textwidth}
Once you have a starting point on the arc each path is found through an iterative process for each row/arc in the table figure \ref{data}:
\begin{itemize}
\item First draw a circle around your origin point with $radius = speed \times time between arcs $
\item where $timebetweenarcs$ is the time difference between the arc that the origin lies on and the next arc. In this example it would be 19:41:00-18:25:27 = 4533s 
\item $radius = 450knots \times 4533s = 1 049km$ 
\item The intercect of both the circle and the arc is your destination point
\item Draw a line between the origin point and the destination point giving you a path
\end{itemize}
The two paths correspond to a nothern and southern trajectory. 
\end{minipage}
\hspace{0.05\textwidth}
\begin{minipage}{0.5\textwidth}
\includegraphics[width=\textwidth]{pathCircle.png}
\captionof{figure}{Example path illustration}
\end{minipage}
\pagebreak

This gives you two possible routes the plane could have taken, one
taking a northern trajectory and another taking a southern trajectory:

\begin{figure}[h]
\centering
\begin{minipage}{0.3\textwidth}
\includegraphics[width=0.93\textwidth]{north1.png}
\end{minipage}
\begin{minipage}{0.3\textwidth}
\includegraphics{north2.png}
\end{minipage}
\hspace{0.2cm}
\begin{minipage}{0.3\textwidth}
\includegraphics[width=0.8\textwidth]{north3.png}
\end{minipage}
\caption{Google earth projection of the northern trajectory}
\end{figure}

\begin{minipage}{0.3\textwidth}
Here is the measured BFO values plotted on a graph against time from the ATSB report.\bigskip

As you can see the BFO values are much more consistent with the predicted BFO values for a southern trajectory.\bigskip 

Which means we can exclude our nothern trajectory as a possible route. 
\end{minipage}
\hspace{0.05\textwidth}
\begin{minipage}{0.65\textwidth}
\includegraphics{traj.png}
\captionof{figure}{BFO projection for nothern and southern routes}
\end{minipage}

## Defining a search area

Now we know the plane must take a southern trajectory the last point of
this on the seventh arc marks the last known position of the plane.

As the plane crosses the seventh arc at 19:29 the handshake is an
unscheduled log on request from the plane. This could mean a loss of
fuel at this point as the emergency power systems would have rebooted
and tried to contact the satelite network. It takes ~ 2 minutes for the
SDU and ADU onboard computers to reboot after a power failure so fuel
loss is expected to be about 2 mins before the failed handshake, so
about 19:27. This time is also consistent with the flights fuel
capabilities knowing its amount of fuel from the last acars at 17:06 and
the time of flight REFERENCE.

So you can take the bearing between the last path and the 7th arc
position. Then go back two minutes in time giving you a distance
assuming a constant speed. This gives you a point slightly north east of
the 7th arc position. As the point of fuel loss (0:17).

\begin{figure}[h]
\centering
\includegraphics[width=.7\textwidth]{lastPoint.png}
\caption{Google earth screenshot of 6th and 7th arcs; fuel loss point; seventh arc position and the most probable location from inmarsat}
\end{figure}

The plane can only go so far from here. The circle shows the maximum
distance before hitting the ocean. This is calculated by an efficient
glide ratio for a 777 of 17:1. Meaning the plane can glide horizontally
about 17 times its altitude. i.e.
\(radius = glide dist = 17 \times 35,000feet = 181 km\). The assumption
that the plane glides is also consistent with some of the wreckage found
showing large intact pieces left REFERENCE.

Knowing the plane keeps a consistent bearing from the 6th arc, throught
the fuel loss point to the 7th arc. It is a resonable assumption that it
stays true to this after the 7th arc. Following the yellow radial line.
Gliding to near the maximum distance at this bearing you can give a
final point for the crash site, where the yellow line intersects the
circle.

\begin{figure}[h]
\centering
\includegraphics[width=.7\textwidth]{lastPath.png}
\caption{Last path estimate, and crash site}
\end{figure}

## Computational Details

### Satelite data

For our BTO analysis we needed accurate satelite data for the position
of the satelite over time. Unfortunatley little information is given
online or in the report about the satlite position.

We decided to use a simulation of the satelite. To predict its drift
over time given the initial conditions. We used intitial conditions
given in the ATSB report. See appendix figure . For time 16:30:00 we
have a position in earth fixed coordinates xyz and velocity x’y’z’.

We used NASA’s open source general mission analysis tool (GMAT) to model
the satelite’s trajectory. This gives us satelite data accurate to the
1/10 of a second. Which is important as the satelite drifts
substantially throughout the flight.

\begin{figure}[h]
\includegraphics{sat1.png}
\caption{Screenshot of GMAT program inputting intial conditions}
\end{figure}

\begin{figure}[h]
\begin{minipage}{.5\textwidth}
\includegraphics{satmap.png}
\end{minipage}
\begin{minipage}{.5\textwidth}
\includegraphics{satdrift.png}
\end{minipage}
\caption{Screenshot of GMAT showing ground track plot and satelite drift}
\end{figure}

We then set the program to give us a report file containing all the
neccessary information:

\begin{figure}[h]
\includegraphics{satdata.png}
\caption{GMAT Report file preview}
\end{figure}

The goal of this project is to take the input data and convert it into a
final path for the plane. Not only that but I wanted the code to run all
in one automatic script so changes could be made to the satelite data or
inmarsat data and the code would be able to run again from scratch. I
also wanted a nice way of visualising this so I used google earth’s kml
library.

Python seemed like an appropriate choice for programming language it
also had all of the libraries I would need. Such as the pandas library
whcih is used for parsing all of the data given by inmarsat see appendix
figure  and the gmat report file into a useable table for calculations.
It was a major challenge to parse them into two usable tables. Then I
had to match the time given in the inmarsat data to a relevant time in
the satelite report file. All of this is done in the getData function
see appendix 

Once we have this condensed into one table, you end up with a table with
about 500 rows. The bias is then calculated for the first half an hour
see . However we ended up using ATSB’s bias value so this function is
now void. The data is then further condensed into a table of seven arcs
giving us figure . See appendix .

I made various functions for plotting lines, points and circles in
google earth. All of which is saved in a kml file which can be opened in
google earth to show a visual representation of the data. I also used
the simplekml library. See appendix 

The next task is drawing the arcs, intitial and final paths. See
appendix  to . An attempt is made at the BFO analysis giving us
deltaFComp and deltaFDown in appendix . Finally the glide ratio is
calculated and a final path estimated saving to the kml file. See
.

# Results and Discussion

| Arc | Date                    |   BTO | BFO |       bias |     Dist | deltaSatAFC | deltaFBias |    deltaFDown |
| --: | :---------------------- | ----: | --: | ---------: | -------: | ----------: | ---------: | ------------: |
|   1 | 2014-03-07 18:25:27.421 | 12520 | 142 | \-0.495679 | 36905.35 |        10.8 |      152.5 | \-1737.185086 |
|   2 | 2014-03-07 19:41:02.906 | 11500 | 111 | \-0.495679 | 36745.42 |       \-1.2 |      152.5 |    \-5.711436 |
|   3 | 2014-03-07 20:41:04.904 | 11740 | 141 | \-0.495679 | 36785.74 |       \-1.3 |      152.5 |   1361.827263 |
|   4 | 2014-03-07 21:41:26.905 | 12780 | 168 | \-0.495679 | 36954.46 |      \-17.9 |      152.5 |   2623.988131 |
|   5 | 2014-03-07 22:41:21.906 | 14540 | 204 | \-0.495679 | 37238.41 |      \-28.5 |      152.5 |   3680.905844 |
|   6 | 2014-03-08 00:10:59.928 | 18040 | 252 | \-0.495679 | 37803.64 |      \-37.7 |      152.5 |   4760.278758 |
|   7 | 2014-03-08 00:19:29.416 | 18400 | 182 | \-0.495679 | 37861.91 |      \-38.0 |      152.5 |   4826.809098 |

Summary table of results

Here is a summary of the output of the python code represented as a
table. With a few columns excluded for the results section. You can find
the full data outputted from the code in appendix .

## Discussion

  - Compare your results with those expected/predicted by theory.
  - Provide reasoned explanation for your results.
  - Compare your results with known results from the literature, if
    appropriate.
  - Give suggestions for further work, where appropriate

# Conclusions

Conclude with a brief sum mary of main findings, and their potential
significance•

# References

  - Use a consistent style – either alphabetic or numeric – to list the
    references cited.
  - In the case of numeric, references should be numbered in the order
    in which they appear in the text. 

\begin{landscape}
\appendix
\counterwithin{figure}{section}
\counterwithin{table}{section}

\section{Appendix tables and figures}

\rowcolors{2}{gray!6}{white}
\begin{table}[!h]

\caption{\label{tab:unnamed-chunk-3}\label{FinalData}Full final data}
\centering
\begin{tabular}[t]{rllrrrrrrr}
\hiderowcolors
\toprule
Arc & Date & DateSat & x & y & z & vx & vy & vz & Lat\\
\midrule
\showrowcolors
1 & 2014-03-07 18:25:27.421 & 2014-03-07 18:25:27.400 & 18136.79 & 38071.78 & 1149.2508 & 0.0018860 & -0.0011539 & 0.0267314 & 1.5626235\\
2 & 2014-03-07 19:41:02.906 & 2014-03-07 19:41:02.900 & 18145.32 & 38067.08 & 1206.1094 & 0.0019099 & -0.0009101 & -0.0018866 & 1.6399145\\
3 & 2014-03-07 20:41:04.904 & 2014-03-07 20:41:04.900 & 18152.42 & 38064.10 & 1158.0904 & 0.0020370 & -0.0007658 & -0.0246225 & 1.5746445\\
4 & 2014-03-07 21:41:26.905 & 2014-03-07 21:41:26.900 & 18160.03 & 38061.35 & 1029.8396 & 0.0021580 & -0.0007836 & -0.0457840 & 1.4003103\\
5 & 2014-03-07 22:41:21.906 & 2014-03-07 22:41:21.900 & 18167.82 & 38058.20 & 831.9831 & 0.0021375 & -0.0009996 & -0.0636594 & 1.1313423\\
\addlinespace
6 & 2014-03-08 00:10:59.928 & 2014-03-08 00:10:59.900 & 18178.16 & 38051.35 & 435.2215 & 0.0015841 & -0.0015748 & -0.0819975 & 0.5919005\\
7 & 2014-03-08 00:19:29.416 & 2014-03-08 00:19:29.400 & 18178.94 & 38050.54 & 393.1532 & 0.0014917 & -0.0016330 & -0.0831191 & 0.5346963\\
\bottomrule
\end{tabular}
\end{table}
\rowcolors{2}{white}{white}

\begin{table}[!h]
\centering\rowcolors{2}{gray!6}{white}

\begin{tabular}{rrrlrrrrrrr}
\hiderowcolors
\toprule
Lat & Lon & Alt & ChType & BTO & BFO & bias & Dist & deltaSatAFC & deltaFBias & deltaFDown\\
\midrule
\showrowcolors
1.5626235 & 64.52761 & 35808.66 & R-Channel RX & 12520 & 142 & -0.495679 & 36905.35 & 10.8 & 152.5 & -1737.185086\\
1.6399145 & 64.51440 & 35809.68 & R-Channel RX & 11500 & 111 & -0.495679 & 36745.42 & -1.2 & 152.5 & -5.711436\\
1.5746445 & 64.50396 & 35808.69 & R-Channel RX & 11740 & 141 & -0.495679 & 36785.74 & -1.3 & 152.5 & 1361.827263\\
1.4003103 & 64.49301 & 35806.16 & R-Channel RX & 12780 & 168 & -0.495679 & 36954.46 & -17.9 & 152.5 & 2623.988131\\
1.1313423 & 64.48162 & 35802.30 & R-Channel RX & 14540 & 204 & -0.495679 & 37238.41 & -28.5 & 152.5 & 3680.905844\\
\addlinespace
0.5919005 & 64.46494 & 35794.61 & R-Channel RX & 18040 & 252 & -0.495679 & 37803.64 & -37.7 & 152.5 & 4760.278758\\
0.5346963 & 64.46350 & 35793.80 & R-Channel RX & 18400 & 182 & -0.495679 & 37861.91 & -38.0 & 152.5 & 4826.809098\\
\bottomrule
\end{tabular}
\rowcolors{2}{white}{white}
\end{table}
\end{landscape}

\begin{figure}
\includegraphics{table1}
\caption{Table from definition of underwater search areas showing example BTO calculation}
\label{table1}
\end{figure}
\begin{figure}
\includegraphics{exampleLog.pdf}
\caption{Log file given provided by inmarsat}
\label{exampleLog}
\end{figure}
\begin{figure}
\includegraphics{biasTable.png}
\caption{BTO calibration table given provided by inmarsat}
\label{biasTable}
\end{figure}

\begin{figure}[h]
\centering
\includegraphics[width=0.5\textwidth]{DeltaAFC.png}
\caption{$\delta f_{sat} + \delta f_{AFC}$ values from ATSB}
\label{DeltaAFC}
\end{figure}

\begin{figure}[h]
\centering
\includegraphics[width=0.5\textwidth]{Heading.png}
\caption{BFO example for 17:07 from ATSB}
\label{Heading}
\end{figure}

\clearpage

# Appendix python code

## Prelude

``` python
import numpy as np
import simplekml
from polycircles import polycircles as pc
import math
import time
import pandas as pd
pd.set_option("display.max_rows",999)
pd.set_option('display.width', 1000)
from datetime import datetime, timedelta
import geopy
from geopy.distance import VincentyDistance
from scipy.spatial import distance
from sympy.solvers import solve
from sympy import Symbol
#Constants
posGES = np.array([-2368.8, 4881.1, -3342.0])
posAES = np.array([-1293.0, 6238.3, 303.5])
c = 299792458/1000#km/s 
iterationConstant = 8000
alt = 10668*1e-3
```

## Parse data function

``` python
#function to parse data from satelite report file and inmarsat csv file
def getData(Time = 3):
    x,y,z,vx,vy,vz,lat,lon,dateSat,alt = ([] for i in range(10))
    #Grab InmarSat Data
    data = pd.read_csv("inmarsat.csv", usecols=[0,8,25,27])
    data.rename(columns={'Time':'Date', 'Frequency Offset (Hz)': 'BFO', 'Burst Timing Offset (microseconds)': 'BTO', 'Channel Type': 'ChType'}, inplace=True)
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y %H:%M:%S.%f')
    #Grab report data
    Report = open("Report.txt", "r")
    lines = Report.readlines()
    #Grab report data
    for i, line in enumerate(lines):
        #if i <=1:
        if "Nov" in line:
            print(line)
            lines.pop(i)
        if i!=0:
            dateSat.append(datetime.strptime(line.split("  ")[0], "%d %b %Y %H:%M:%S.%f"))
            x.append(line.split()[4])
            y.append(line.split()[5])
            z.append(line.split()[6])
            vx.append(line.split()[7])
            vy.append(line.split()[8])
            vz.append(line.split()[9])
            lat.append(line.split()[10])
            lon.append(line.split()[11])
            alt.append(line.split()[12])
    dateSatd = []
    xd = []
    yd = []
    zd = []
    vxd = []
    vyd = []
    vzd = []
    lond = []
    latd = []
    altd = []
    data = data[pd.notnull(data['BTO'])]
    data = data.reset_index(drop=True)
    data = data[pd.notnull(data['BTO'])]
    data = data.reset_index(drop=True)
    for i in range(len(data)):
        for j in range(len(dateSat)):
            if abs(dateSat[j]-data['Date'][i])<=timedelta(0,0,0,50):
                dateSatd.append(dateSat[j])
                xd.append(x[j])
                yd.append(y[j])
                zd.append(z[j])
                vxd.append(vx[j])
                vyd.append(vy[j])
                vzd.append(vz[j])
                latd.append(lat[j])
                lond.append(lon[j])
                altd.append(alt[j])
                del dateSat[:j] 
                del x[:j]
                del y[:j]
                del z[:j]
                del vx[:j]
                del vy[:j]
                del vz[:j]
                del lat[:j]
                del lon[:j]
                del alt[:j]
                break
    data["DateSat"] = pd.Series(dateSatd)
    data["x"] = pd.Series(xd)
    data["y"] = pd.Series(yd)
    data["z"] = pd.Series(zd)
    data["vx"] = pd.Series(vxd)
    data["vy"] = pd.Series(vyd)
    data["vz"] = pd.Series(vzd)
    data["Lat"] = pd.Series(latd)
    data["Lon"] = pd.Series(lond)
    data["Alt"] = pd.Series(altd)
    data = data[['Date', 'DateSat', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'Lat', 'Lon', 'Alt', 'ChType', 'BTO', 'BFO']]#rearrange columns
    data.x = data.x.astype(float)
    data.y = data.y.astype(float)
    data.z = data.z.astype(float)
    data.vx = data.vx.astype(float)
    data.vy = data.vy.astype(float)
    data.vz = data.vz.astype(float)
    data.Lon = data.Lon.astype(float)
    data.Lat = data.Lat.astype(float)
    data.Alt = data.Alt.astype(float)
    data.BTO = data.BTO.astype(float)
    data.BFO = data.BFO.astype(float)
    return data
```

## Miscellaneous functions

``` python
#recursive asks for use input
def inputR(inputText, wantedTextList):
    inp = False
    while inp == False:
        string = input(inputText)
        if string in wantedTextList:inp = True
    return string 
# returns bias given data
def getBias(posSat):
    distSatGES = np.linalg.norm(posSat-posGES, axis = 1)
    distSatAES = np.linalg.norm(posSat-posAES, axis = 1)
    biasR = []
    biasT = []
    for i in range(len(data)):
        if data['ChType'][i]=="R-Channel RX":
            biasR.append((data['BTO'][i]*1e-6) - 2*(distSatAES[i]+distSatGES[i])/c )
        if data['ChType'][i]=="T-Channel RX":
            biasT.append((data['BTO'][i]*1e-6) - 2*(distSatAES[i]+distSatGES[i])/c )
    bias = []
    biasRn = 0
    biasTn = 0
    for i in range(len(data)):
        if data["Date"][i]==datetime(2014,3,7,16,41,52,907000):#TakeOff
            meanBiasR = np.mean(biasR)
            meanBiasT = np.mean(biasT)
            meanBiasT = -0.495679
            meanBiasR=meanBiasT
            print("The bias used is: ", meanBiasT, "s")
        if data["Date"][i]<=datetime(2014,3,7,16,29,52,406000):#preTakeOff
            if data['ChType'][i]=="R-Channel RX":
                bias.append(biasR[biasRn])
                biasRn = biasRn+1
            elif data['ChType'][i]=="T-Channel RX":
                bias.append(biasT[biasTn])
                biasTn = biasTn+1
        else:#postTakeOff   
            if data['ChType'][i]=="R-Channel RX": bias.append(meanBiasR)
            elif data['ChType'][i]=="T-Channel RX": bias.append(meanBiasT)
    bias = pd.Series(bias)
    return bias, distSatGES
#gives indexes for data matching the arc dates 
def getArcDates():
    arcDate = []
    arcIndexes = []             
    arcDate.append(datetime(2014,3,7,18,25,27))
    arcDate.append(datetime(2014,3,7,19,41,00))
    arcDate.append(datetime(2014,3,7,20,41,00))
    arcDate.append(datetime(2014,3,7,21,41,24))
    arcDate.append(datetime(2014,3,7,22,41,19))
    arcDate.append(datetime(2014,3,8,0,10,58))
    arcDate.append(datetime(2014,3,8,0,19,29))
    for i in range(len(arcDate)):
        for j in range(len(data)):
            if abs(data["Date"][j]-arcDate[i])<=timedelta(0,5):
                arcIndexes.append(j)    
    return arcIndexes
#converts latitude and longitude to earth centered earth fixed coordinates
def lla_to_ecef(lat, lon, alt):
    import pyproj
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    x, y, z = pyproj.transform(lla, ecef, lon, lat, alt, radians=False)
    return x, y, z
#converts ecef to lat lon coords
def ecef_to_lla(x, y, z):
    import pyproj
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)
    return lat, lon, alt
```

``` python
#Main code start
pd.options.mode.chained_assignment = None
print("getting data...")
```

    ## getting data...

``` python
data = getData()
print("done")
```

    ## done

``` python
arcDates = getArcDates()
data["BTO"][arcDates[0]] = data.iloc[arcDates[0]].loc["BTO"]-4600
data["BTO"][arcDates[6]] = data.iloc[arcDates[6]].loc["BTO"]-4600
data.to_csv("Data.csv")
data = pd.read_csv("Data.csv")
data = data.drop(['Unnamed: 0'], axis=1)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S.%f')
data['DateSat'] = pd.to_datetime(data['DateSat'], format='%Y-%m-%d %H:%M:%S.%f')
arcDates = getArcDates()
#Some more data assignment
data["bias"], distSatGES = getBias(data.as_matrix(['x','y','z']))
```

    ## The bias used is:  -0.495679 s

``` python
data["Dist"] = (0.5*c*((data["BTO"].values*1e-6)-data["bias"].values)) - distSatGES 
deltaSatAFC = np.zeros(len(data))
deltaFBias = np.full(len(data), 152.5)
data["deltaSatAFC"] = pd.Series(np.asarray(deltaSatAFC))
data["deltaFBias"] = pd.Series(np.asarray(deltaFBias))
data.deltaSatAFC = data.deltaSatAFC.astype(float)
data.deltaFBias = data.deltaFBias.astype(float)
data["deltaSatAFC"][arcDates[0]] = 10.8
data["deltaSatAFC"][arcDates[1]] = -1.2
data["deltaSatAFC"][arcDates[2]] = -1.3
data["deltaSatAFC"][arcDates[3]] = -17.9
data["deltaSatAFC"][arcDates[4]] = -28.5
data["deltaSatAFC"][arcDates[5]] = -37.7
data["deltaSatAFC"][arcDates[6]] = -38.0
data = data[data.deltaSatAFC != 0]
data = data.reset_index(drop=True)
```

## Google earth kml functions

``` python
def drawPoint(Name, Lat, Lon, Alt):
    pnt = kml.newpoint(name= Name)
    pnt.coords = [(Lon, Lat, Alt)]
    pnt.altitudemode = 'relativeToGround'
    return 1
def drawCircle(Name, Lat, Lon, Radius, color):
    circle = pc.Polycircle(latitude=Lat, longitude=Lon, radius=Radius, number_of_vertices=iterationConstant)
    pol = kml.newpolygon(name=Name, outerboundaryis=circle.to_kml())
    pol.style.polystyle.color ="000000ff"   # Transparent 
    pol.style.linestyle.color = color
    pol.altitudemode = 'absoluteAltitude'
    pol.tessellate = 1 
    return circle
def drawLine(Name, originLat, originLon, destLat, destLon, color):
    ls = kml.newlinestring(name = Name)
    ls.style.linestyle.color = color
    ls.coords = [(originLon, originLat), (destLon, destLat)]
    return 1
```

## Drawing the arcs

``` python
kml = simplekml.Kml()
drawPoint("Satposition", np.mean(data["Lat"].values), np.mean(data["Lon"].values),357860)
arcIndexes = arcDates
arcNo = 0
circles = []
#draw arcs
for i in range(len(data)):
    arcNo = arcNo+1
    a = data["Dist"][i]
    b = np.square(data["x"][i])+np.square(data["y"][i])+np.square(data["z"][i])
    b = np.sqrt(b)
    c = 6371+alt#+73
    #c = 6371+alt+50
    pheta = np.square(b)+np.square(c)-np.square(a)
    pheta = pheta / (2*b*c)
    pheta = np.arccos(pheta)
    radius = c*pheta
    datetime(2014,3,7,16,29,52,406000)
    radius = radius*1000
    circles.append(drawCircle("Arc"+str(arcNo), data["Lat"][i], data["Lon"][i], radius, simplekml.Color.white))
```

## Drawing the intitial path

``` python
#find path between arcs given a direction north or south  
def findShortest(name, radius, origin, alt, circle, direction):
    distArr = []
    circle = circle.to_lat_lon()
    lastDist = 99999
    for i in range(len(circle)):
        destination = geopy.Point(circle[i][0], circle[i][1], alt)
        distance = VincentyDistance(origin, destination).meters 
        dist = distance-radius
        if (lastDist>0) and (dist<0) and (direction=="North"):
            minDist = dist
            j = i
        if (lastDist<0) and (dist>0) and (direction=="South"):
            minDist = dist
            j = i
        lastDist = dist
    return geopy.Point(circle[j][0], circle[j][1], alt)
def drawPath(origin, dest, time, no):
    if time.minute<10:
        drawPoint(str(time.hour)+":0"+str(time.minute), dest.latitude, dest.longitude, alt)
    else:
        drawPoint(str(time.hour)+":"+str(time.minute), dest.latitude, dest.longitude, alt)
    drawLine("Path"+str(no), origin.latitude, origin.longitude, dest.latitude, dest.longitude, simplekml.Color.red)
    return 1 
#get destination given origin times and breaing
def getDest(origin, lastTime, time, bearing, radius):
    dest = VincentyDistance(kilometers=radius*1e-3).destination(origin, bearing)
    return dest
alt = alt*1000
speed = 231.5#450knots
time = datetime(2014,3,7,17,6,43)
origin = geopy.Point(2.7, 101.7, 0)
dest = geopy.Point(5.27, 102.79, alt)
drawPath(origin, dest, time, 1) 
origin = dest
lastTime = time
time = datetime(2014, 3, 7, 17, 21, 13)
deltaT = abs(lastTime-time).total_seconds()
radius = speed*deltaT
dest = getDest(origin, lastTime, time, 25, radius)
drawPath(origin, dest, time, 2)
origin = dest
lastTime = time
time = datetime(2014,3,7,17,52,27)
dest = geopy.Point(5.2, 100.2, alt)
drawPath(origin, dest, time, 3)
origin = dest
lastTime = time
time = datetime(2014,3,7,18,22,12)
dest = geopy.Point(6.65, 96.34, alt)
drawPath(origin, dest, time, 4)
speed = 320#Max speed
origin = dest
lastTime = time
time = data["Date"][0]
deltaT = abs(lastTime-time).total_seconds()
radius = speed*deltaT
destArr = []
dest = findShortest("test", radius, origin, alt, circles[0], "North")   
destArr.append(dest)
firstArcPos = dest
drawPath(origin, dest, time, 5)
```

## Drawing paths between the arcs

``` python
speed = 231.5#450knots
#draw paths
for i in range(0,6):
    origin = dest
    deltaT = abs(data["Date"][i+1]-data["Date"][i]).total_seconds()
    radius = speed*deltaT
    time = data["Date"][i+1]
    dest = findShortest("test", radius, origin, alt, circles[i+1], "South")
    destArr.append(dest)
    drawPath(origin, dest, time, 5+i)
    #drawCircle('test', origin.latitude, origin.longitude, radius, simplekml.Color.green)
    #draw green circle for example
origin = dest
lastTime = time
time = lastTime-timedelta(0,120) 
deltaT = abs(lastTime-time).total_seconds()
radius = speed*deltaT
dest = getDest(origin, lastTime, time, 7.70, radius)
drawPath(origin, dest, time, 11)
```

## BFO analysis attempt

``` python
#give a table of delta F comps
def getFComp(posPl, speed, posSat):
    v = v/1000
    #sat = [0,64.5,35786*1e3]
    #sat = lla_to_ecef(sat[0], sat[1], sat[2])
    #sat = np.array(sat)*1e-3
    s = posSat-posPl
    vs = np.dot(v,s)
    vs = vs/np.linalg.norm(s)
    Fup = 1646.6525*1e6
    deltaFComp = Fup*(((c+vs)/c)-1)
    return deltaFComp
#BFO Analysis
deltaFDown = []
for i in range(len(data)):
    v = np.array([data["vx"][i], data["vy"][i], data["vz"][i]], dtype=float)
    s = np.array([data["x"][i], data["y"][i], data["z"][i]], dtype=float)
    s = s-posGES
    vS = np.dot(v, s)/np.linalg.norm(s)
    FDown = 3615.1525e6
    deltaFDown.append(FDown*((c/(c+vS))-1))
data["deltaFDown"] = pd.Series(deltaFDown)
data.deltaFDown = data.deltaFDown.astype(float)
```

## Glide code and saving the kml file

``` python
maxAlt = 10668#35kfeet
glideDist = maxAlt*16.995
drawCircle("Glide", dest.latitude, dest.longitude, glideDist, simplekml.Color.white) 
drawPoint("Their location", -35.6, 92.8, 0)
print(data)
#save to kml file ready for importing to google earth
```

    ##                      Date                 DateSat             x             y            z        vx        vy        vz       Lat        Lon           Alt        ChType      BTO    BFO      bias          Dist  deltaSatAFC  deltaFBias   deltaFDown
    ## 0 2014-03-07 18:25:27.421 2014-03-07 18:25:27.400  18136.788690  38071.780267  1149.250781  0.001886 -0.001154  0.026731  1.562623  64.527615  35808.658697  R-Channel RX  12520.0  142.0 -0.495679  36905.345735         10.8       152.5 -1737.185086
    ## 1 2014-03-07 19:41:02.906 2014-03-07 19:41:02.900  18145.322644  38067.080600  1206.109395  0.001910 -0.000910 -0.001887  1.639914  64.514401  35809.676311  R-Channel RX  11500.0  111.0 -0.495679  36745.423272         -1.2       152.5    -5.711437
    ## 2 2014-03-07 20:41:04.904 2014-03-07 20:41:04.900  18152.415261  38064.097851  1158.090407  0.002037 -0.000766 -0.024623  1.574644  64.503959  35808.689335  R-Channel RX  11740.0  141.0 -0.495679  36785.744457         -1.3       152.5  1361.827263
    ## 3 2014-03-07 21:41:26.905 2014-03-07 21:41:26.900  18160.033945  38061.351242  1029.839567  0.002158 -0.000784 -0.045784  1.400310  64.493009  35806.160960  R-Channel RX  12780.0  168.0 -0.495679  36954.463239        -17.9       152.5  2623.988131
    ## 4 2014-03-07 22:41:21.906 2014-03-07 22:41:21.900  18167.817569  38058.202812   831.983119  0.002137 -0.001000 -0.063659  1.131342  64.481623  35802.301035  R-Channel RX  14540.0  204.0 -0.495679  37238.408842        -28.5       152.5  3680.905844
    ## 5 2014-03-08 00:10:59.928 2014-03-08 00:10:59.900  18178.157195  38051.354149   435.221535  0.001584 -0.001575 -0.081998  0.591901  64.464937  35794.610366  R-Channel RX  18040.0  252.0 -0.495679  37803.640202        -37.7       152.5  4760.278758
    ## 6 2014-03-08 00:19:29.416 2014-03-08 00:19:29.400  18178.941079  38050.536935   393.153216  0.001492 -0.001633 -0.083119  0.534696  64.463497  35793.797327  R-Channel RX  18400.0  182.0 -0.495679  37861.914631        -38.0       152.5  4826.809098

``` python
kml.save("Flight.kml")
#save data
data.to_csv("FinalData.csv")
```
