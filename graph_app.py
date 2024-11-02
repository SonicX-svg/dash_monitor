import pandas as pd
import os
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Загружаем данные из файла iostat и преобразуем столбец 'Time' в формат datetime
df = pd.read_csv('iostat_cleaned.csv')
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
df = df.sort_values(by='Time')  # Сортируем по времени для корректного отображения

# Получаем все параметры из DataFrame
parameters = df.columns[2:].tolist()  # Предполагается, что первые два столбца - это 'Time' и 'Device'
devices = df['Device'].unique()

percent_parameters = [param for param in parameters if '%' in param]  # Получаем параметры с '%'
percent_parameters_options = [{'label': 'all', 'value': 'all'}] + [{'label': param, 'value': param} for param in percent_parameters]

# Путь к папке с файлами nmon
nmon_csv_path = 'csv'  # Папка с nmon CSV-файлами

# Определяем параметры для nmon файлов
nmon_parameters_dict = {
    'CPU001.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU002.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU003.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU004.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU005.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU006.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU007.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU008.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU009.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU010.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU011.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU012.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU013.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU014.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU015.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU016.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'CPU_ALL.csv': ['User%', 'Sys%', 'Wait%', 'Idle%', 'Steal%'],
    'DISKREAD.csv': ['loop0', 'loop1', 'loop2', 'loop3', 'loop4', 'loop5', 'loop6', 'loop7', 
                     'nvme0n1', 'nvme0n1p1', 'nvme0n1p2', 'nvme0n1p3', 'nvme0n1p4', 
                     'nvme0n1p5', 'nvme1n1', 'nvme1n1p1', 'nvme1n1p2', 'nvme1n1p3'],
    'DISKWRITE.csv': ['loop0', 'loop1', 'loop2', 'loop3', 'loop4', 'loop5', 'loop6', 'loop7', 
                      'nvme0n1', 'nvme0n1p1', 'nvme0n1p2', 'nvme0n1p3', 'nvme0n1p4', 
                      'nvme0n1p5', 'nvme1n1', 'nvme1n1p1', 'nvme1n1p2', 'nvme1n1p3'],
    'DISKBUSY.csv': ['loop0', 'loop1', 'loop2', 'loop3', 'loop4', 'loop5', 'loop6', 'loop7', 
                     'nvme0n1', 'nvme0n1p1', 'nvme0n1p2', 'nvme0n1p3', 'nvme0n1p4', 
                     'nvme0n1p5', 'nvme1n1', 'nvme1n1p1', 'nvme1n1p2', 'nvme1n1p3'],
    'DISKBSIZE.csv': ['loop0', 'loop1', 'loop2', 'loop3', 'loop4', 'loop5', 'loop6', 'loop7', 
                      'nvme0n1', 'nvme0n1p1', 'nvme0n1p2', 'nvme0n1p3', 'nvme0n1p4', 
                      'nvme0n1p5', 'nvme1n1', 'nvme1n1p1', 'nvme1n1p2', 'nvme1n1p3'],
    'MEM.csv': ['JFS Filespace %Used', 'sonikx-3-0', '/dev', '/run', '/', '/snap/bare/5', 
                '/snap/chatgpt-desktop/8', '/snap/core/17200', '/snap/core18/2829', 
                '/snap/core18/2846', '/snap/core20/2379', '/snap/core22/1621', 
                '/snap/core24/490', '/snap/dbeaver-ce/327', '/snap/discord/212', 
                '/snap/dmidecode-tool/3', '/snap/firefox/5091', '/snap/firefox/5134', 
                '/snap/firmware-updater/127', '/snap/firmware-updater/147', 
                '/snap/gnome-3-28-1804/198', '/snap/gnome-3-38-2004/143', 
                '/snap/gnome-42-2204/172', '/snap/gnome-42-2204/176', 
                '/snap/gnome-46-2404/42', '/snap/gnome-46-2404/48', 
                '/snap/gtk-common-themes/1535', '/snap/intellij-idea-community/535', 
                '/snap/intellij-idea-community/537', '/snap/kdf/104', '/snap/kdf/105', 
                '/snap/kf5-5-111-qt-5-15-11-core22/7', '/snap/kf5-5-113-qt-5-15-11-core22/1', 
                '/snap/kf6-core22/38', '/snap/kf6-core22/39', '/snap/libreoffice/324', 
                '/snap/libreoffice/326', '/snap/mesa-2404/143', '/snap/ngrok/207', 
                '/snap/obs-studio/1302', '/snap/postman/286', '/snap/qt-common-themes/10', 
                '/snap/qt-common-themes/8', '/snap/snap-store/1173', '/snap/pygpt/264', 
                '/snap/snap-store/1216', '/snap/snapd/21465', '/snap/snapd/21759', 
                '/snap/snapd-desktop-integration/247', '/snap/snapd-desktop-integration/253', 
                '/var/snap/firefox/common/host-hunspell', '/snap/zoom-client/230', 
                '/snap/core20/2434', '/snap/dbeaver-ce/328'],
    'NET.csv': ['lo-read-KB/s', 'enp6s0-read-KB/s', 'wlo1-read-KB/s', 'br-f7a4a2ec8a65-read-KB/s', 
                 'docker0-read-KB/s', 'br-1b94b2df3def-read-KB/s', 'br-85886957e939-read-KB/s', 
                 'br-bb13e4125e24-read-KB/s', 'br-c00aa61d0677-read-KB/s', 'vmnet1-read-KB/s', 
                 'vmnet8-read-KB/s', 'veth2f49389-read-KB/s', 'veth9e86400-read-KB/s', 
                 'veth2aaa955-read-KB/s', 'veth6d60ff8-read-KB/s', 'lo-write-KB/s', 
                 'enp6s0-write-KB/s', 'wlo1-write-KB/s', 'br-f7a4a2ec8a65-write-KB/s', 
                 'docker0-write-KB/s', 'br-1b94b2df3def-write-KB/s', 'br-85886957e939-write-KB/s', 
                 'br-bb13e4125e24-write-KB/s', 'vmnet1-write-KB/s', 'vmnet8-write-KB/s', 
                 'veth2f49389-write-KB/s', 'veth9e86400-write-KB/s', 'veth2aaa955-write-KB/s', 
                 'veth6d60ff8-write-KB/s'],
    'NETPACKET.csv': ['lo-read/s', 'enp6s0-read/s', 'wlo1-read/s', 'br-f7a4a2ec8a65-read/s', 
                      'docker0-read/s', 'br-1b94b2df3def-read/s', 'br-85886957e939-read/s', 
                      'br-bb13e4125e24-read/s', 'br-c00aa61d0677-read/s', 'vmnet1-read/s', 
                      'vmnet8-read/s', 'veth2f49389-read/s', 'veth9e86400-read/s', 
                      'veth2aaa955-read/s', 'veth6d60ff8-read/s', 'lo-write/s', 
                      'enp6s0-write/s', 'wlo1-write/s', 'br-f7a4a2ec8a65-write/s', 
                      'docker0-write/s', 'br-1b94b2df3def-write/s', 'br-85886957e939-write/s', 
                      'br-bb13e4125e24-write/s', 'vmnet1-write/s', 'vmnet8-write/s', 
                      'veth2f49389-write/s', 'veth9e86400-write/s', 'veth2aaa955-write/s', 
                      'veth6d60ff8-write/s'],
    'PROC.csv': ['Runnable', 'Blocked', 'pswitch', 'syscall', 'read', 'write', 'fork', 
                  'exec', 'sem', 'msg'],
    'vm.csv': ['Memory', 'nr_dirty', 'nr_writeback', 'nr_unstable', 'nr_page_table_pages', 
                'nr_mapped', 'nr_slab_reclaimable', 'pgpgin', 'pgpgout', 'pswpin', 
                'pswpout', 'pgfree', 'pgactivate', 'pgdeactivate', 'pgfault', 
                'pgmajfault', 'pginodesteal', 'slabs_scanned', 'kswapd_steal', 
                'kswapd_inodesteal', 'pageoutrun', 'allocstall', 'pgrotated', 
                'pgalloc_high', 'pgalloc_normal', 'pgalloc_dma', 'pgrefill_high', 
                'pgrefill_normal', 'pgrefill_dma', 'pgsteal_high', 'pgsteal_normal', 
                'pgsteal_dma', 'pgscan_kswapd_high', 'pgscan_kswapd_normal', 
                'pgscan_kswapd_dma', 'pgscan_direct_high', 'pgscan_direct_normal', 
                'pgscan_direct_dma']
}

app = Dash(__name__)

# Задаем стили приложения
app.layout = html.Div(style={'backgroundColor': '#5c5c5e', 'color': 'white'}, children=[
    dcc.Tabs([
        dcc.Tab(label='Iostat Data', style={'backgroundColor': '#5c5c5e'}, selected_style={'backgroundColor': '#7a7a7a'}, children=[
            dcc.Dropdown(
                id='iostat-device-dropdown',
                options=[{'label': 'all', 'value': 'all'}] + [{'label': device, 'value': device} for device in devices],
                value='all',
                style={'backgroundColor': '#5c5c5e', 'color': 'white', 'border': '1px solid white'}
            ),
            dcc.Dropdown(
                id='iostat-parameter-dropdown',
                options=[{'label': param, 'value': param} for param in parameters],
                value=parameters[0] if parameters else None,
                style={'backgroundColor': '#5c5c5e', 'color': 'white', 'border': '1px solid white'}
            ),
            dcc.Dropdown(
                id='iostat-percent-parameter-dropdown',
                options=percent_parameters_options,
                value='%idle',  # Значение по умолчанию
                style={'backgroundColor': '#5c5c5e', 'color': 'white', 'border': '1px solid white'}
            ),
            dcc.Graph(id='iostat-graph', style={'backgroundColor': '#5c5c5e'}),
            dcc.Graph(id='iostat-percent-graph', style={'backgroundColor': '#5c5c5e'})
        ]),
        dcc.Tab(label='Nmon Data', style={'backgroundColor': '#5c5c5e'}, selected_style={'backgroundColor': '#7a7a7a'}, children=[
            dcc.Dropdown(
                id='nmon-parameter-dropdown',
                options=[{'label': file, 'value': file} for file in nmon_parameters_dict.keys()],
                value='CPU_ALL.csv',  # Значение по умолчанию установлено на PROC.csv
                style={'backgroundColor': '#5c5c5e', 'color': 'white', 'border': '1px solid white'}
            ),
            dcc.Dropdown(
                id='nmon-characteristics-dropdown',
                options=[],
                multi=True,
                value=nmon_parameters_dict['CPU_ALL.csv'],  # Устанавливаем все параметры по умолчанию
                style={'backgroundColor': '#5c5c5e', 'color': 'white', 'border': '1px solid white'}
            ),
            dcc.Graph(id='nmon-graph', style={'backgroundColor': '#5c5c5e'})
        ])
    ])
])

@app.callback(
    Output('iostat-graph', 'figure'),
    [Input('iostat-device-dropdown', 'value'),
     Input('iostat-parameter-dropdown', 'value'),
     Input('iostat-percent-parameter-dropdown', 'value')]
)
def update_iostat_graph(selected_device, selected_param, selected_percent_param):
    fig = go.Figure()

    # Logic to select data for plotting based on selected parameters
    if selected_device == 'all':
        for device in devices:
            device_data = df[df['Device'] == device]
            fig.add_trace(go.Scatter(
                x=device_data['Time'],
                y=device_data[selected_param],
                mode='lines',
                name=f"{device} - {selected_param}"
            ))
    else:
        device_data = df[df['Device'] == selected_device]
        fig.add_trace(go.Scatter(
            x=device_data['Time'],
            y=device_data[selected_param],
            mode='lines',
            name=f"{selected_device} - {selected_param}"
        ))

    # Configure axes and title
    fig.update_layout(
        title='Iostat Data',
        xaxis=dict(title='Time', type='date'),  # Ensure x-axis is in date format
        yaxis_title='Value',
        plot_bgcolor='#5c5c5e',  # Цвет фона графика
        paper_bgcolor='#5c5c5e',  # Цвет бумаги
        font=dict(color='white')  # Цвет шрифта
    )
    
    return fig

@app.callback(
    Output('iostat-percent-graph', 'figure'),
    [Input('iostat-device-dropdown', 'value'),
     Input('iostat-percent-parameter-dropdown', 'value')]
)
def update_percent_graph(selected_device, selected_percent_param):
    fig = go.Figure()

    if selected_percent_param != 'all':
        if selected_device == 'all':
            for device in devices:
                device_data = df[df['Device'] == device]
                fig.add_trace(go.Scatter(
                    x=device_data['Time'],
                    y=device_data[selected_percent_param],
                    mode='lines',
                    name=f"{device} - {selected_percent_param} (percent)",
                    showlegend=False
                ))
        else:
            device_data = df[df['Device'] == selected_device]
            fig.add_trace(go.Scatter(
                x=device_data['Time'],
                y=device_data[selected_percent_param],
                mode='lines',
                name=f"{selected_device} - {selected_percent_param} (percent)",
                showlegend=False
            ))

    fig.update_layout(
        title='Iostat Percent Data',
        xaxis=dict(title='Time', type='date'),
        yaxis_title='Percent Value',
        plot_bgcolor='#5c5c5e',  # Цвет фона графика
        paper_bgcolor='#5c5c5e',  # Цвет бумаги
        font=dict(color='white')  # Цвет шрифта
    )

    return fig

@app.callback(
    Output('nmon-characteristics-dropdown', 'options'),
    Input('nmon-parameter-dropdown', 'value')
)
def update_nmon_characteristics(selected_file):
    if selected_file in nmon_parameters_dict:
        return [{'label': char, 'value': char} for char in nmon_parameters_dict[selected_file]]
    return []

@app.callback(
    Output('nmon-graph', 'figure'),
    [Input('nmon-parameter-dropdown', 'value'),
     Input('nmon-characteristics-dropdown', 'value')]
)
def update_nmon_graph(selected_file, selected_characteristics):
    fig = go.Figure()
    nmon_df = pd.read_csv(os.path.join(nmon_csv_path, selected_file))

    time_columns = nmon_df.columns[nmon_df.columns.str.contains('sonikx-3-0')]
    print("Найденные столбцы с 'sonikx-3-0' в файле:", selected_file, ":", time_columns.tolist())

    if not time_columns.empty:
        nmon_df['Time'] = pd.to_datetime(nmon_df[time_columns[0]], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        for index, characteristic in enumerate(selected_characteristics):
            if characteristic in nmon_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=nmon_df['Time'],
                        y=nmon_df[characteristic],
                        mode='lines',
                        name=characteristic,
                        line=dict(color=px.colors.qualitative.Set1[index % len(px.colors.qualitative.Set1)])
                    )
                )
        
        fig.update_layout(
            title=f'Nmon Data for {selected_file}',
            xaxis_title='Time',
            yaxis_title='Value',
            plot_bgcolor='#5c5c5e',  # Цвет фона графика
            paper_bgcolor='#5c5c5e',  # Цвет бумаги
            font=dict(color='white')  # Цвет шрифта
        )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
