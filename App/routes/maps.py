import folium
from flask import render_template
from . import routes
from App.extension import db
from sqlalchemy import func
from App.model import dbmodel


@routes.route("/map")
def map():
    # query1 = db.session.query(func.ST_AsEncodedPolyline(dbmodel.RoadLine.geometry)).all()
    query = db.session.query(func.ST_X(dbmodel.Roads.geometry), func.ST_Y(dbmodel.Roads.geometry))
    my_map = folium.Map(location=[1.4240728935508973,103.83719841454955], zoom_start=15)
    folium.TileLayer('stamentoner').add_to(my_map)
    # for data1 in query1:
    #     # folium.PolyLine(data1).add_to(my_map)
    #     # folium.PolyLine(data1).add_to(my_map)

    i = 0
    tooltip = "Click me!"
    # for data in query:
    #     new = []
    #     new.append(data[1])
    #     new.append(data[0])
    #     # shp = to_shape(data)
    #     folium.Marker(
    #         new, popup="<i<HE/i>", tooltip=tooltip
    #     ).add_to(my_map)
    #     # print(data[0])
    #     # folium.GeoJson(data).add_to(my_map)
    #     if i == 2000:
    #         break
    #     i+=1

    folium.Marker([1.4297664934963341,103.83583237010218]).add_to(my_map)
    folium.Marker([1.420522241820387,103.83768179301586]).add_to(my_map)
    # folium.GeoJson(query.ST_AsGeoJSON(), name="G" + str(i)).add_to(my_map)
    my_map.save("App/templates/map2.html")
    return render_template("map.html")
