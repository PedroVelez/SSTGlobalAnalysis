d=load('DemarcacionCAN.txt');
fidDem = fopen('DemarcacionCAN_Leaflet.txt','w');
fprintf(fidDem,'    var polygonCAN = L.polygon([\n');
for i1=1:length(d)
    fprintf(fidDem,'      [%4.2f , %4.2f],\n',d(i1,2),d(i1,1));
end
fprintf(fidDem,'    ]).addTo(map);\n');