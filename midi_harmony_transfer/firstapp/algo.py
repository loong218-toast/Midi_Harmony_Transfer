from distutils.log import error
import pretty_midi
import pandas as pd
import numpy as np
import musicpy as mp
import plotly.express as px
import os
import warnings
#from firstapp.views import main
import datetime
import os
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from midi_harmony_transfer.settings import BASE_DIR


class midi_harm_transfer:
    def __init__(self, upload1='', upload2=''):
        
        #Delete .mid file in file directory
        self.filedirectory_name = os.path.dirname(os.path.dirname(__file__))
        self.filedirectory_list = os.listdir(self.filedirectory_name)
        for item in self.filedirectory_list:
            if item.endswith(".mid") and item != 'output.mid':
                os.remove(os.path.join(self.filedirectory_name, item))

        self.filedirectory = str(BASE_DIR)
        f = open(self.filedirectory + str("\progress.txt"), "w")
        f.write("0")
        f.close()
        #print(self.filedirectory)

        self.midi_file_main = upload1
        self.midi_file_transfer = upload2
        self.midi_main = None
        self.midi_second = None

        self.notes = pd.Series(['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'], name='notes')

        if self.midi_file_main != '':

            if 'InMemoryUploadedFile' in str(type(self.midi_file_main)):

                main_path = default_storage.save(str(self.midi_file_main), ContentFile(self.midi_file_main.read()))
                main_file = os.path.join(settings.MEDIA_ROOT, main_path)
                print(main_file)

            #Ignore false positive warning
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.midi_main = pretty_midi.PrettyMIDI(main_file)

            #Dataframe preprocessing
            self.df_main = pd.DataFrame(self.midi_main.get_piano_roll())
            self.df_main = self.df_main.replace(np.arange(1, self.df_main.max().max() + 1), 1)
            self.df_main = self.df_main.iloc[::-1]
            self.df_main = self.df_main.reset_index(drop=True)

        #Dataframe indexes initialization
        pitch_index = np.array([])
        note_index = np.array([])
        for n in range(int(128 / 12)):
            pitch_index = np.append(pitch_index, np.arange(0, 12)[::-1])
            note_index = np.append(note_index, self.notes)
            
        pitch_index = np.insert(pitch_index, 0, np.arange(0, 8)[::-1], axis=0)
        note_index = np.insert(note_index, 0, self.notes[0:9], axis=0)
        pitch_index = pitch_index.astype('int32')
        pitch_index = pd.Series(pitch_index, name='pitch_index')

        if self.midi_file_transfer != '':
            if 'InMemoryUploadedFile' in str(type(self.midi_file_transfer)):
                transfer_path = default_storage.save(str(self.midi_file_transfer), ContentFile(self.midi_file_transfer.read()))
                second_file = os.path.join(settings.MEDIA_ROOT, transfer_path)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.midi_second = pretty_midi.PrettyMIDI(second_file)

            self.df_second = pd.DataFrame(self.midi_second.get_piano_roll())
            self.df_second = self.df_second.replace(np.arange(1, self.df_second.max().max() + 1), 1)
            self.df_second = self.df_second.iloc[::-1]
            self.df_second = self.df_second.reset_index(drop=True)
            

        if self.midi_file_main != '':
            self.df_main = pd.concat([self.df_main, pitch_index], axis=1).set_index('pitch_index')
        if self.midi_file_transfer != '':
            self.df_second = pd.concat([self.df_second, pitch_index], axis=1).set_index('pitch_index')

        
    def midi_verify(self, midi):
        if midi == -2:
            midi = 0
        elif midi == -1:
            midi = 1
        
        if midi == 0 or midi == self.midi_main:
            return self.midi_main
        elif midi == 1 or midi == self.midi_second:
            return self.midi_second
    
    def df_verify(self, midi):
        if midi == 0 or midi == self.midi_main:
            return self.df_main
        elif midi == 1 or midi == self.midi_second:
            return self.df_second
    
    #Count notes from midi
    def notes_count(self, midi=0):
        #midi = self.midi_verify(midi)
        notes_count = np.array([])
        for ins in range(len(midi.instruments)):
            notes_count = np.append(notes_count, len(midi.instruments[ins].notes))
        return notes_count.sum()
        
    #Notes distribution
    def dist(self, midi=0, visual=False):
        exist = True
        if midi == 0:
            midi = self.midi_main
        elif midi == 1:
            midi = self.midi_second
        else:
            try:
                midi = pretty_midi.PrettyMIDI(midi)
            except:
                print("file doesn't exist")
                exist = False

        if exist == True:
            pitch_dist = pd.Series(midi.get_pitch_class_histogram(), name='pitch_dist').round(6)
            pitch_df = pd.concat([self.notes, pitch_dist], axis=1)
            pitch_df['pitch_dist'] = round(pitch_df['pitch_dist'] * len(midi.instruments[0].notes))
            pitch_df['pitch_dist'] = pitch_df['pitch_dist'] / pitch_df['pitch_dist'].sum() * 100

            #Show second midi with same key as main midi
            # if midi == self.midi_second:
            #     second_key = pitch_df[pitch_df['notes'] == self.key(1)[0]].index[0]
            #     pitch_df = pd.concat([pitch_df[pitch_df.index >= second_key], pitch_df[pitch_df.index < second_key]],
            #                              axis=0)
            #     pitch_df = pitch_df.reset_index(drop=True)
            #     pitch_df['notes'] = self.notes

            if visual == True:
                fig = px.bar(pitch_df, x='notes', y='pitch_dist')
                fig.update_layout()
                fig.show()
            
            return pitch_df
    
    #Notes grouping
    def group(self, midi=0, visual=False):
        midi = self.midi_verify(midi)
        df = self.df_verify(midi)
        
        pitch_freq = np.array([])
        notes_multi = np.array([])
        time = np.array([])
        threshold = np.array([])
        exceed_threshold = np.array([])
        interval = 10
        

        #moving_dataframe finds rapid changes in midi
        for num in range(round((df.shape[1] - 49 ) / interval)):

            moving_df = df.loc[:, num*interval:num*interval+49]
            moving_df = moving_df.set_index([np.arange(0, 128), moving_df.index.values])

            moving_df_group = moving_df.groupby(level=[1]).sum()
            moving_df_value = moving_df[(moving_df == 1).any(axis=1)]

            moving_df_value_25 = moving_df_value.iloc[:round(len(moving_df_value) * 25/100), :]
            moving_df_value_25_75 = moving_df_value.iloc[round(len(moving_df_value) * 25/100):round(len(moving_df_value) * 75/100), :]
            moving_df_value_75_100 = moving_df_value.iloc[round(len(moving_df_value) * 75/100):, :]

            moving_df_value_25 = moving_df_value_25.replace(1, 1)
            moving_df_value_25_75 = moving_df_value_25_75.replace(1, 3)
            moving_df_value_75_100 = moving_df_value_75_100.replace(1, 5)

            moving_df_value = pd.concat([moving_df_value_25, moving_df_value_25_75, moving_df_value_75_100])
            moving_df_value = moving_df_value.groupby(level=1).sum()
            moving_df_value = moving_df_value.iloc[0:, :].sum(axis=1)

            for n in range(len(self.notes)):

                if n in moving_df_value.index:
                    pitch_freq = np.append(pitch_freq, moving_df_value.loc[n])
                else:
                    pitch_freq = np.append(pitch_freq, 0)

                notes_multi = np.append(notes_multi, self.notes[n])
                time = np.append(time, num)

            pitch_freq_threshold = np.sum(pitch_freq[num*12:num*12+12]) * 10/100
            threshold = np.append(threshold, np.full(shape=12, fill_value=pitch_freq_threshold))
            exceed_threshold = np.append(exceed_threshold, np.greater(pitch_freq[num*12:num*12+12], pitch_freq_threshold))
            

        pitch_freq = pd.Series(pitch_freq, name='pitch_dist')
        notes_multi = pd.Series(notes_multi, name='notes')
        time = pd.Series(time, name='time')
        threshold = pd.Series(threshold, name='threshold')
        exceed_threshold = pd.Series(exceed_threshold, name='exceed_threshold')

        pitch_df = pd.concat([notes_multi, pitch_freq, time, threshold, exceed_threshold], axis=1)
        pitch_df['exceed_threshold_prev'] = pitch_df['exceed_threshold'].shift(12)
        pitch_df['separator'] = np.where(((pitch_df['exceed_threshold_prev'] == 0) & (pitch_df['exceed_threshold'] == 1)),
                                            True, False)
        
        pitch_df_separator_true = pitch_df[pitch_df['separator'] == True].copy()
        pitch_df_separator_true['time_distance'] = pitch_df_separator_true['time'].diff()
        pitch_df_separator_true = pitch_df_separator_true[pitch_df_separator_true['time_distance'] >= pitch_df_separator_true['time_distance'].mean()]
        
        pitch_df_td = pd.concat([pitch_df, pitch_df_separator_true.loc[:, ['time', 'time_distance']]], axis=1)
        pitch_df_td = pitch_df_td[(pitch_df_td['separator'] == True) & (pitch_df_td['time_distance'] > 0)]
        pitch_df_td = pitch_df_td.loc[:,~pitch_df_td.columns.duplicated()]
        pitch_df_td['time_seconds'] = pitch_df_td['time'] / (len(pitch_df) / 12) * self.midi_main.get_end_time()
        
        #visualize data if true
        if visual == True:
            fig = px.bar(pitch_df, x='notes', y='pitch_dist', animation_frame='time')
            fig.show()
            pd.set_option('display.min_rows', 50)
            pd.set_option('display.max_rows', 50)
            pd.options.plotting.backend = "plotly"
            
            #display(pitch_df_separator_true['time_distance'].plot(kind='hist'))
            #display(pitch_df_td)
            
            fig = px.scatter_3d(pitch_df, x='notes', y='time', z='pitch_dist', color='notes',size_max=10)
            fig.update_layout(title='3D pitch_dist', autosize=False,
                              width=500, height=500,
                              margin=dict(l=80, r=80, b=65, t=65))
            fig.show()

        #Grouping
        notes_arr = np.zeros((int(self.notes_count(midi).sum()), 6))
        notes_arr2 = np.zeros((int(self.notes_count(midi).sum()), 1), dtype=np.dtype('U5'))
        note_id = np.array([])
        count = 0
        pattern = r'[0-9]'
        for ins in range(len(midi.instruments)):
            for n, note in enumerate(midi.instruments[ins].notes):
                notes_arr[count] = [note.start, note.end, note.pitch, note.velocity, ins, n]
                note_name = str(pretty_midi.note_number_to_name(note.pitch))
                notes_arr2[count] = str(~mp.note(re.sub(pattern, '', note_name))).replace('4', '')
                count+=1

        notes_arr2 = notes_arr2.flatten()
        notes_df = pd.DataFrame(notes_arr)
        notes_df2 = pd.Series(notes_arr2)
        notes_df = pd.concat([notes_df, notes_df2], axis=1)
        notes_df.columns = ['start', 'end', 'pitch', 'velocity', 'instrument', 'note_id', 'note_name']

        group_notes_all = pd.DataFrame()
        group = np.array([])
        index = np.array([])
        time_sec = np.array(pitch_df_td['time_seconds'])
        time_sec = np.concatenate(([-1], time_sec, [99]))

        for n in range(time_sec.shape[0]):
            try:
                group_notes = notes_df[(notes_df['start'] >= time_sec[n]) & (notes_df['start'] < time_sec[n + 1])].copy()

            except IndexError:
                break
            
            group = np.append(group, np.full(len(group_notes), n))
            index = np.append(index, np.arange(len(group_notes)))
            group_notes_all = pd.concat([group_notes_all, group_notes], axis=0)
        
        group_notes_all['group'] = group
        group_notes_all['index'] = index
        group_notes_all = group_notes_all.set_index(['group', 'index', 'note_id'])

        return group_notes_all
        
    #Finding key
    def key(self, midi=0):
        
        midi = self.midi_verify(midi)
        pitch_dist = pd.Series(midi.get_pitch_class_histogram(), name='pitch_dist').round(6)
        pitch_df = pd.concat([self.notes, pitch_dist], axis=1)
        pitch_df['pitch_dist'] = round(pitch_df['pitch_dist'] * len(midi.instruments[0].notes))
        midi_key = pitch_df.nlargest(7, 'pitch_dist').iloc[:, 0]
        pattern = r'[0-9]'
        
        for note in pitch_df['notes']:
            compare_Mkey = mp.S(f'{note} major').standard()
            compare_Mkey_relativenote = re.sub(pattern, '', str(mp.S(f'{note} major').relative_key().notes[0]))
            if "#" in compare_Mkey_relativenote:
                compare_Mkey_relativenote = re.sub(pattern, '', str(~mp.note(compare_Mkey_relativenote)))

            for l in range(len(compare_Mkey)):
                if "#" in str(compare_Mkey[l]):
                    compare_Mkey[l] = re.sub(pattern, '', str(~mp.note(compare_Mkey[l])))
                if "Cb" in str(compare_Mkey[l]):
                    compare_Mkey[l] = "B"
                if "Fb" in str(compare_Mkey[l]):
                    compare_Mkey[l] = "E"

            if set(midi_key) == set(compare_Mkey):
                key = [compare_Mkey[0], '']
                
                minor_pitch_dist = pitch_df[pitch_df['notes'] == compare_Mkey_relativenote].iloc[0, 1]
                major_pitch_dist = pitch_df[pitch_df['notes'] == note].iloc[0, 1]
                
                if minor_pitch_dist > major_pitch_dist: #Calculate major or minor key
                    compare_mkey = mp.S(f'{compare_Mkey_relativenote} minor').standard()
                    for l in range(len(compare_mkey)):
                        if "#" in str(compare_mkey[l]):
                            compare_mkey[l] = re.sub(pattern, '', str(~mp.note(compare_mkey[l])))
                        if "Cb" in str(compare_mkey[l]):
                            compare_mkey[l] = "B"
                        if "Fb" in str(compare_mkey[l]):
                            compare_mkey[l] = "E"
                    key = [compare_mkey[0], 'm']
                    
                break

            else:
                key = [midi_key.iloc[0], '']
        
        return key
     
    #Distribution matching algorithm
    def dist_matching(self, path='' ,visual=False):
        epoch = 40
        learning_rate = 0.1
        minimum_step_size = 0.5 #the distance between step size and local minimum
        midi_main = self.midi_main
        output_mid = '\output.mid'
        path = self.filedirectory + output_mid
        self.error_sum_list = np.zeros(epoch)
        written = False
        progress_cancel_file = self.filedirectory + str("\progress_cancelled.txt")

        if os.path.exists(progress_cancel_file):
                os.remove(progress_cancel_file)
        print('start')
        for loop in range(epoch):
            if written == True:
                midi_main = pretty_midi.PrettyMIDI(path)

            if os.path.exists(progress_cancel_file):
                print('terminated')
                os.remove(progress_cancel_file)
                break
                
            #midi_main
            pitch_dist_main = pd.Series(midi_main.get_pitch_class_histogram(), name='pitch_dist').round(6)
            pitch_df_main = pd.concat([self.notes, pitch_dist_main], axis=1)
            pitch_df_main['pitch_dist'] = round(pitch_df_main['pitch_dist'] * self.notes_count(midi_main))
            
            #midi second
            pitch_dist_second = pd.Series(self.midi_second.get_pitch_class_histogram(), name='pitch_dist').round(6)
            pitch_df_second = pd.concat([self.notes, pitch_dist_second], axis=1)
            pitch_df_second['pitch_dist'] = round(pitch_df_second['pitch_dist'] * self.notes_count(self.midi_second))

            #Change second midi key to the same as midi_main
            first_key = pitch_df_second[pitch_df_second['notes'] == self.key(0)[0]].index[0]
            second_key = pitch_df_second[pitch_df_second['notes'] == self.key(1)[0]].index[0]
            index_series = pd.Series(list(pitch_df_second[pitch_df_second.index >= first_key].index.values
                                         ) + list(pitch_df_second[pitch_df_second.index < first_key].index.values), name="index")

            pitch_df_second['notes'] = pd.concat([pitch_df_second[pitch_df_second.index >= first_key].iloc[:, 0], pitch_df_second[pitch_df_second.index < first_key].iloc[:, 0]],
                                 axis=0, ignore_index=True)
            pitch_df_second = pd.concat([pitch_df_second, index_series], axis=1)
            pitch_df_second = pitch_df_second.set_index(index_series).sort_index().drop("index", axis=1)

            pitch_dist_all = pd.concat([pitch_df_main['pitch_dist'], pitch_df_second['pitch_dist']], axis=1)
            pitch_dist_all.columns = ['main', 'second']
            pitch_dist_all['main'] = pitch_dist_all['main'] / pitch_dist_all['main'].sum() * 100
            pitch_dist_all['second'] = pitch_dist_all['second'] / pitch_dist_all['second'].sum() * 100
            pitch_dist_all['error_type'] = np.where(((pitch_dist_all['main'] - pitch_dist_all['second']) <= 0
                                                    ), 'negative', 'positive')
            pitch_dist_all['pitch_exist'] = np.where(pitch_dist_all['second'] != 0, True, False)

            #Calculate errors between 2 datasets in a dataframe
            pitch_dist_all['error'] = (pitch_dist_all['main'] - pitch_dist_all['second'])**2
            error_sum = pitch_dist_all['error'].sum()
            
            #Notes with errors ranked by priority
            seven_dist_ranked = pitch_dist_all.nlargest(7, 'main')
            for count, index in enumerate(pitch_dist_all.nlargest(7, 'main').index.values):
                if seven_dist_ranked['error_type'].iloc[count] == 'negative':
                    continue
                
                #Start from notes with highest distribution
                largest_error_index = index
                largest_error_index_error = seven_dist_ranked['error'].iloc[count]
                #Wider left and right side
                pitch_dist_all_wide = pd.concat([pitch_dist_all.iloc[-2:], pitch_dist_all, pitch_dist_all.iloc[:2]])

                #Moving nearby notes of the main note
                pitch_dist_near = pitch_dist_all_wide.iloc[largest_error_index : largest_error_index + 5]
                pitch_dist_near = pitch_dist_near.reset_index()
                pitch_dist_near = pitch_dist_near.set_index(np.arange(-2, 3))

                pitch_dist_near = pitch_dist_near[pitch_dist_near['error_type'] == 'negative']
                pitch_dist_near = pitch_dist_near[pitch_dist_near['pitch_exist'] == True]
                
                try:
                    #No error means it is very well optimized and break the loop
                    pitch_dist_near_largest_error_index = pitch_dist_near.nlargest(1, 'error').index.values[0]
                except:
                    break
                
                #Step size = learning rate * derivative of actual(second) with respect to predicted(main)
                step_size = learning_rate * 2 * (seven_dist_ranked['main'].iloc[count] - seven_dist_ranked['second'].iloc[count])
                if step_size < minimum_step_size:
                    continue
                
                #Select group notes
                group_notes_arr = np.array([])
                group_notes = self.group()
                group_notes = group_notes[group_notes['note_name'].str.contains(self.notes[largest_error_index])]
                if not group_notes.empty:
                    #Randomly select groups by most error notes
                    selected_groups = []
                    group_notes_index = 0
                    avoid_duplicated_group_notes_index_list = []
                    if step_size < 1:
                        step_size = 1
                    for group in range(round(step_size)):
                        for index in range(50):
                            group_notes_index = np.random.choice(np.unique(np.array(group_notes.index.get_level_values(level=0))))
                            if not group_notes_index in avoid_duplicated_group_notes_index_list:
                                
                                break
                        
                        selected_group_notes = group_notes.xs(group_notes_index, level=0,
                                                                  axis=0, drop_level=False)
                        #display(selected_group_notes)
                        avoid_duplicated_group_notes_index_list.append(group_notes_index)
                        selected_groups.append(selected_group_notes)
                            
                    for selected_group in selected_groups:
                        for n in range(len(selected_group)):
                            midi_main.instruments[int(selected_group['instrument'].iloc[n])
                                                 ].notes[int(selected_group.index.get_level_values(level=2)[n])
                                                        ].pitch += pitch_dist_near_largest_error_index
                    break
                else:
                    continue

            
            print(f'Error : {error_sum}')
            #Update midi file
            midi_main.write(path)
            written = True
            self.error_sum_list[loop] = error_sum
            
            global progress
            progress = round((loop + 1) / epoch * 100)
            print('progress : ' + str(progress))

            f = open(self.filedirectory + str("\progress.txt"), "w")
            f.write(str(progress))
            f.close()

        #return error_sum



    def tempo(self, midi):
        midi = self.midi_verify(midi)
        return round(midi.estimate_tempo() / 2)

    def time_length(self, midi):
        midi = self.midi_verify(midi)
        return datetime.timedelta(seconds = round(midi.get_end_time()))


    def velocity(self, midi, visual=False):
    
        midi = self.midi_verify(midi)
        
        self.df_velocity = pd.DataFrame(midi.get_piano_roll())
        self.df_velocity = self.df_velocity.iloc[::-1]
        self.df_velocity = self.df_velocity.reset_index(drop=True)
        
        pd.set_option('display.min_rows', 128)
        pd.set_option('display.max_rows', 128)
        
        vel_arr = np.array([])
        
        for n in self.df_velocity.columns:
            self.series_vel = self.df_velocity[n].drop_duplicates(keep='first').to_numpy()
            
            if self.series_vel.shape[0] > 1:
                self.series_vel = self.series_vel[self.series_vel != 0]
                
            self.series_vel = np.mean(self.series_vel)
            
            vel_arr = np.append(vel_arr, self.series_vel)
        vel_arr = vel_arr[::60]
        #print(vel_arr.shape)
        
        if visual == True:
            fig = px.line(x=np.arange(vel_arr.shape[0]), y=vel_arr, title='Velocity')
            fig.show()

        return dict(zip(np.arange(vel_arr.shape[0]).astype('str'), vel_arr))

    def terminator(self):
        f = open(self.filedirectory + str("\progress_cancelled.txt"), "w")
        f.write('progress_cancelled')
        f.close()