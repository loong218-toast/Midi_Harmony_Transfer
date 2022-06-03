# Midi Harmony Transfer
 Midi Harmony Transfer program with custom machine learning algorithm. <br/>
 
 This web app is not hosted yet.

# Results

https://user-images.githubusercontent.com/77558802/171025482-114480a3-8184-4667-9b37-15114cffd001.mp4

(with Pokemon Litteroot Town.mid)

https://user-images.githubusercontent.com/77558802/171030672-d1f6a5a9-041f-4284-966b-0c69a334b1ac.mp4

(with never gonna give you up.mid)

https://user-images.githubusercontent.com/77558802/171202693-76c53fc2-f403-473d-944a-b096469edd34.mp4

(with la-campanella.mid)

# UI
![Screenshot 2022-05-30 215543](https://user-images.githubusercontent.com/77558802/171017313-a4bff8a3-b4e7-4855-8e30-bd5a4c063011.png)


# Algorithm

The algorithm compares two musical note distributions of two different Midi files(.mid), then one will adjusts its distribution to try to fit another one. <br/>
The distribution fitting process is done by moving groups of notes which are majority, and move to those notes that are minority.
The algorithm also creates relationships between musical notes by grouping them with indexes, and those notes move together. <br/>


<img src="https://user-images.githubusercontent.com/77558802/171204455-c665dea4-0f6a-4cba-ba56-d599975e251b.png" width=40%>

(Dataframe behind the algorithm)

The notes only move a half step or a whole step, so them move a small distance in each epoch.

<img src="https://user-images.githubusercontent.com/77558802/171206988-655a1242-bc34-47e8-add5-5fae2584aee6.png" width=40%>
(Learning curve of the first Midi music listed above) <br/>
<br/>
The Learning curve is not smooth, but that is fine. Consider the fact that each note can only be moved by a certain interval, notes allocation is conducted within limited range each time. <br/>
<br/>
The whole process is optimized by gradient descent. More groups of notes are processed at initial state, and it decreases as its distribution is closer to another one (because step size is smaller).

## Notes Grouping
The algorithm constantly monitor the changing distribution of the music each timeframe with anomaly detection. When the distribution changes drastically (it hits an adaptive threshold), The algorithm groups those notes that happen before the spike. This is used to simulate how human hear the chord changes in music. The downside of this method is that, it needs collect enough data first so that it detects chord changes, but this can cause some delay.

## Other Features
This web app can identify key, tempo, and time length of a Midi file. Music modes and tempo changes are not supported yet.

# Resources Used
Python : Django, Pandas, Numpy, Prettymidi, Musicpy, Plotly, Re <br/>
Web dev : Javascript (React, Jquery, Axios, Chart.js), HTML (Bootstrap), CSS
