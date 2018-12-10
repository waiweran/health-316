from plotly import plotly, tools, exceptions
import requests
import json

username = 'augustning'
accountkey = 'fjFaA6Af6vDjuZmjLNa0'

plotly.sign_in(username, accountkey)
auth = requests.auth.HTTPBasicAuth(username, accountkey)
headers = {'Plotly-Client-Platform': 'python'}


def make_states_plot(plot_locations, plot_data, tooltip_labels, colorscale_label, plot_title):
	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

	data = [ dict(
	        type='choropleth',
	        colorscale = scl,
	        autocolorscale = False,
	        locations = plot_locations,
	        z = plot_data,
	        locationmode = 'USA-states',
	        text = tooltip_labels,
	        marker = dict(
	            line = dict (
	                color = 'rgb(0,0,0)',
	                width = 2
	            ) ),
	        colorbar = dict(
	            title = colorscale_label)
	        ) ]

	layout = dict(
	        title = plot_title,
	        geo = dict(
	            scope='usa',
	            projection=dict( type='albers usa' ),
	            showlakes = False,
	            lakecolor = 'rgb(255, 255, 255)'),
	             )

	fig = dict( data=data, layout=layout )
	try:
		return tools.get_embed(plotly.plot(fig, auto_open=False))
	except exceptions.PlotlyRequestError as e:
		return "Plot limit reached: " + str(e) + " \n\nPlease contact HealthInsights to purchase a premium plan."

def make_countries_plot(plot_locations, plot_data, tooltip_labels, colorscale_label, plot_title):
	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

	data = [ dict(
	        type = 'choropleth',
	        locations = plot_locations,
	        z = plot_data,
	        text = tooltip_labels,
	        colorscale = scl,
	        autocolorscale = False,
	        marker = dict(
	            line = dict (
	                color = 'rgb(0,0,0)',
	                width = 2
	            ) ),
	        colorbar = dict(
	            title = colorscale_label),
	      ) ]

	layout = dict(
	    title = plot_title,
	    geo = dict(
	        showframe = False,
	        showcoastlines = False,
	        projection = dict(
	            type = 'Mercator'
	        )
	    )
	)

	fig = dict( data=data, layout=layout )
	try:
		return tools.get_embed(plotly.plot(fig, auto_open=False))
	except exceptions.PlotlyRequestError as e:
		return "Plot limit reached: " + str(e) + " \n\nPlease contact HealthInsights to purchase a premium plan."
