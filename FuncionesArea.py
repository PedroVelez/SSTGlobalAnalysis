#>>>> ---------------------------------------------------------------
def seleccionaArea(titulo_short,DS):

    if titulo_short == 'LEB':
        slicelatitude=slice(35.5,42.75)
        slicelongitude=slice(358,368)
        sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
        PolygonDemarTransformed = transform_polygon(polygon_demar(titulo_short))     
        mask = np.array([[point_in_polygon(lon,lat,PolygonDemarTransformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
        sst_unmasked = sst
        sst = sst.where(mask)
        print('>>>>> '+titulo_short)        

    elif  titulo_short == 'NOR':
        slicelatitude=slice(41.5,46.9)
        slicelongitude=slice(346,360)
        sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
        PolygonDemarTransformed = transform_polygon(polygon_demar(titulo_short))     
        mask = np.array([[point_in_polygon(lon,lat,PolygonDemarTransformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
        sst_unmasked = sst
        sst = sst.where(mask)
        print('>>>>> '+titulo_short)        
            
    elif  titulo_short == 'CAN':
        slicelatitude=slice(24,32.5)
        slicelongitude=slice(335,350)
        sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
        PolygonDemarTransformed = transform_polygon(polygon_demar(titulo_short))     
        mask = np.array([[point_in_polygon(lon,lat,PolygonDemarTransformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
        sst_unmasked = sst
        sst = sst.where(mask)
        print('>>>>> '+titulo_short)    

    elif  titulo_short == 'SUD':
        slicelatitude=slice(35.5,37.5)
        slicelongitude=slice(352,354.5)
        sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
        PolygonDemarTransformed = transform_polygon(polygon_demar(titulo_short))     
        mask = np.array([[point_in_polygon(lon,lat,PolygonDemarTransformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
        sst_unmasked = sst
        sst = sst.where(mask)
        print('>>>>> '+titulo_short)

    elif  titulo_short == 'ESA':
        slicelatitude=slice(35.5,37)
        slicelongitude=slice(354,358.5)
        sst=DS.sst.sel(lat=slicelatitude).sel(lon=slicelongitude)
        PolygonDemarTransformed = transform_polygon(polygon_demar(titulo_short))     
        mask = np.array([[point_in_polygon(lon,lat,PolygonDemarTransformed) 
            for lon in sst.lon.values] 
            for lat in sst.lat.values])
        sst_unmasked = sst
        sst = sst.where(mask)
        print('>>>>> '+titulo_short)
        
    elif  titulo_short == 'IBICan':
        sst = DS.sst.sel(lat=slice(20, 47),lon=slice(325,360))
        # Para blanquear el mediterraneo
        lat_point_list = [40, 40, 30, 30, 40]
        lon_point_list = [354.5, 360, 360, 354.5, 354.5]
        polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
        polygon = transform_polygon(polygon_geom)
        mask = np.array([[point_in_polygon(lon,lat,polygon) 
                    for lon in sst.lon.values] 
                    for lat in sst.lat.values])  
        sst = sst.where(~mask) 
        print('>>>>> '+titulo_short)

    elif titulo_short == 'GO':
        sst = DS.sst.sel(lat=slice( -75, 75)) 
        print('>>>>> '+titulo_short)

    return sst     
#----------------------------------------------------------------<<<<

#>>>> ---------------------------------------------------------------
# Define a transformation to ensure the polygon's CRS matches
# Transform the polygon to match the DataArray CRS if needed
def polygon_demar(titulo_short):
    
    demCoord = []
    longDem, latiDem = [], []
    
    with open('./data/Demarcacion'+titulo_short+'.txt', 'r') as f:
        for line in f:
        # Split the line by whitespace and append the values
            longitude, latitude = map(float, line.split())
            longitude=longitude+360
            longDem.append(longitude)
            latiDem.append(latitude)
            demCoord.append((longitude,latitude))
    Polygon = Polygon(demCoord)    
    return Polygon
#----------------------------------------------------------------<<<<


#>>>> ---------------------------------------------------------------
def transform_polygon(polygon, src_crs='epsg:4326', tgt_crs='epsg:4326'):
    proj = pyproj.Transformer.from_proj(pyproj.Proj(src_crs), pyproj.Proj(tgt_crs), always_xy=True)
    return transform(lambda x, y: proj.transform(x, y), polygon)
#----------------------------------------------------------------<<<<

#>>>> ---------------------------------------------------------------
def point_in_polygon(lon, lat, polygon):
        point = Point(lon, lat)
        return polygon.contains(point)
#----------------------------------------------------------------<<<<

