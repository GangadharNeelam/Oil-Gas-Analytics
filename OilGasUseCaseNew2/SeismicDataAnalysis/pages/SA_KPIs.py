from dependencies import *
import segyio
import scipy.signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def SA_KPIs():
    # Define a caching function for loading seismic data
    @st.cache_data
    def load_seismic_data(filename, header_location):
        with segyio.open(filename, xline=header_location) as segyfile:
            return segyio.tools.cube(segyfile)

    # Define a caching function for calculating amplitude envelope
    @st.cache_data
    def calculate_amplitude_envelope(seismic_slice):
        return np.abs(hilbert(seismic_slice))


    # Define a caching function for loading fault data
    @st.cache_data
    def load_fault_data(filename, header_location):
        with segyio.open(filename, xline=header_location) as segyfile:
            return segyio.tools.cube(segyfile)

    # Load seismic data
    filename_pp = "./issap20_Pp.sgy"
    filename_ai = "./issap20_AI.sgy"
    filename_fault = "./issap20_Fault.sgy"

    seismic = load_seismic_data(filename_pp, header_location=181)
    ai = load_seismic_data(filename_ai, header_location=181)
    fault = load_fault_data(filename_fault, header_location=181)

    f"Number of inlines: {seismic.shape[0]}, crosslines: {seismic.shape[1]}, samples: {seismic.shape[2]}"

    selected_data = st.selectbox("Select Data:", ["Seismic Data", "AI Data", "Fault Data"])

    if selected_data == "Seismic Data":
        selected_graph = st.radio("Select Graph Type:", ["Seismic Section", "Amplitude Envelope"])
        selected_depth = st.slider("Select Depth:", min_value=0, max_value=750, step=1, value=375)

        if selected_graph == "Seismic Section":
            # Visualize a seismic section at the selected depth using Plotly
            seismic_slice = seismic[:, :, selected_depth]

            fig = go.Figure(data=go.Heatmap(z=seismic_slice.T, colorscale='RdBu'))
            fig.update_layout(title=f'Seismic Section at Depth {selected_depth}',
                            xaxis_title='Crossline',
                            yaxis_title='Inline')
            # st.plotly_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

        elif selected_graph == "Amplitude Envelope":
            # Calculate and visualize the amplitude envelope using scipy.signal.hilbert with Plotly
            seismic_slice = seismic[:, :, selected_depth]
            amplitude_envelope = calculate_amplitude_envelope(seismic_slice)

            fig = go.Figure(data=go.Heatmap(z=amplitude_envelope.T, colorscale='Viridis'))
            fig.update_layout(title=f'Amplitude Envelope at Depth {selected_depth}',
                            xaxis_title='Crossline',
                            yaxis_title='Inline')
            st.plotly_chart(fig, use_container_width=True)

    elif selected_data == "AI Data":
        # Radio buttons for choosing the type of graph
        selected_graph = st.radio("Select Graph Type:", ["AI Section", "Histogram", "3D Visualization"])
        selected_depth = st.slider("Select Depth:", min_value=0, max_value=750, step=1, value=375)

        if selected_graph == "AI Section":
            # Visualize AI section at the selected depth using Plotly
            ai_slice = ai[:, :, selected_depth]

            fig = go.Figure(data=go.Heatmap(z=ai_slice.T, colorscale='Viridis'))
            fig.update_layout(title=f'AI Section at Depth {selected_depth}',
                            xaxis_title='Crossline',
                            yaxis_title='Inline')
            st.plotly_chart(fig, use_container_width=True)

        elif selected_graph == "Histogram":
            # Plot histogram of AI values at the selected depth using Plotly
            ai_values = ai[:, :, selected_depth].flatten()

            fig = go.Figure(data=[go.Histogram(x=ai_values, marker=dict(color='green'))])
            fig.update_layout(title=f'AI Histogram at Depth {selected_depth}',
                            xaxis_title='Acoustic Impedance',
                            yaxis_title='Frequency')
            st.plotly_chart(fig, use_container_width=True)

        elif selected_graph == "3D Visualization":
            # Create a 3D visualization of AI data using Plotly
            inline, xline = np.meshgrid(np.arange(ai.shape[1]), np.arange(ai.shape[0]))
            ai_values_3d = ai[:, :, selected_depth]

            fig = go.Figure(data=[go.Surface(z=ai_values_3d, colorscale='Viridis')])
            fig.update_layout(title=f'3D Visualization of (Acoustic Impedance)AI at Depth {selected_depth}',
                            scene=dict(xaxis_title='Inline',
                                        yaxis_title='Crossline',
                                        zaxis_title='Acoustic Impedance'))
            st.plotly_chart(fig, use_container_width=True)

    elif selected_data == "Fault Data":
        # Radio buttons for choosing the type of graph
        selected_graph = st.radio("Select Graph Type:", ["Fault Section", "3D Visualization"])
        selected_depth = st.slider("Select Depth:", min_value=0, max_value=750, step=1, value=375)

        if selected_graph == "Fault Section":
            # Visualize a fault section at the selected depth using Plotly
            fault_slice = fault[:, :, selected_depth]

            fig = go.Figure(data=go.Heatmap(z=fault_slice.T, colorscale='Viridis'))
            fig.update_layout(title=f'Fault Section at Depth {selected_depth}',
                            xaxis_title='Crossline',
                            yaxis_title='Inline')
            st.plotly_chart(fig, use_container_width=True)

        elif selected_graph == "3D Visualization":
            # Create a 3D visualization of fault data using Plotly
            inline, xline = np.meshgrid(np.arange(fault.shape[1]), np.arange(fault.shape[0]))
            fault_values_3d = fault[:, :, selected_depth]

            fig = go.Figure(data=[go.Surface(z=fault_values_3d, colorscale='Viridis')])
            fig.update_layout(title=f'3D Visualization of Fault Data at Depth {selected_depth}',
                            scene=dict(xaxis_title='Inline',
                                        yaxis_title='Crossline',
                                        zaxis_title='Fault Data'))
            st.plotly_chart(fig, use_container_width=True)
