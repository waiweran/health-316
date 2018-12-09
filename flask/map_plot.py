from plotly import plotly, tools
import requests

username = 'liuharryk'
accountkey = 'WkCtIN7yoxMvGpuyCzew'

plotly.sign_in(username, accountkey)


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
	except PLotlyRequestError:
		delete_files(filetype_to_delete='plot')
		delete_files(filetype_to_delete='grid')
		return tools.get_embed(plotly.plot(fig, auto_open=False))

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
	except PLotlyRequestError:
		delete_files(filetype_to_delete='plot')
		delete_files(filetype_to_delete='grid')
		return tools.get_embed(plotly.plot(fig, auto_open=False))

def get_pages(page_size):
    url = 'https://api.plot.ly/v2/folders/all?user='+username+'&page_size='+str(page_size)
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code != 200:
        return
    page = json.loads(response.content)
    yield page
    while True:
        resource = page['children']['next'] 
        if not resource:
            break
        response = requests.get(resource, auth=auth, headers=headers)
        if response.status_code != 200:
            break
        page = json.loads(response.content)
        yield page
        
def delete_files(page_size=500, filetype_to_delete='plot'):
    for page in get_pages(page_size):
        for x in range(0, len(page['children']['results'])):
            fid = page['children']['results'][x]['fid']
            res = requests.get('https://api.plot.ly/v2/files/' + fid, auth=auth, headers=headers)
            res.raise_for_status()
            if res.status_code == 200:
                json_res = json.loads(res.content)
                if json_res['filetype'] == filetype_to_delete:
                    # move to trash
                    requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', auth=auth, headers=headers)

