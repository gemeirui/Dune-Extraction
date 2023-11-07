# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-11-06 16:54:04
"""
import arcpy
from arcpy.sa import *
from sys import argv

def Extraction(Neighbourhood="Rectangle 95 95 CELL", DEM_tif="C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\Pyramid Megadune DEM.tif"):  # Extraction

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    # Model Environment settings
    with arcpy.EnvManager(extent="-400644.301673142 4733556.81095962 -154204.189588109 4963903.67501775 PROJCS["Asia_Lambert_Conformal_Conic",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",105.0],PARAMETER["Standard_Parallel_1",30.0],PARAMETER["Standard_Parallel_2",62.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]", scratchWorkspace=r"C:\Users\WINDOWS\Desktop\Dune Extraction\data\mid data", workspace=r"C:\Users\WINDOWS\Desktop\Dune Extraction"):
        Output_Location = "D:\\沙丘提取\\实验数据\\沙丘提取实验_new\\实验12\\金字塔型沙山"

        # Process: Slope (Slope) (3d)
        Slope_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Slope.tif"
        arcpy.ddd.Slope(in_raster=DEM_tif, out_raster=Slope_tif, output_measurement="DEGREE", z_factor=1, method="PLANAR", z_unit="METER")
        Slope_tif = arcpy.Raster(Slope_tif)

        # Process: Project Raster (Project Raster) (management)
        Slope_Pro_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Slope_Pro.tif"
        arcpy.management.ProjectRaster(in_raster=Slope_tif, out_raster=Slope_Pro_tif, out_coor_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]", resampling_type="NEAREST", cell_size="35.4429514436888 35.4429514436888", geographic_transform=[], Registration_Point="", in_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", vertical="NO_VERTICAL")
        Slope_Pro_tif = arcpy.Raster(Slope_Pro_tif)

        # Process: Reclassify (Reclassify) (3d)
        Reclass_Slope_1_5_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Reclass_Slope_1_5.tif"
        arcpy.ddd.Reclassify(in_raster=Slope_Pro_tif, reclass_field="VALUE", remap="0 1.500000 1;1.500000 999 NODATA", out_raster=Reclass_Slope_1_5_tif, missing_values="NODATA")
        Reclass_Slope_1_5_tif = arcpy.Raster(Reclass_Slope_1_5_tif)

        # Process: Raster to Polygon (Raster to Polygon) (conversion)
        Slope_Patches_shp = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Slope Patches.shp"
        with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
            arcpy.conversion.RasterToPolygon(in_raster=Reclass_Slope_1_5_tif, out_polygon_features=Slope_Patches_shp, simplify="SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

        # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
        Slope_patches1_shp = arcpy.management.CalculateGeometryAttributes(in_features=Slope_Patches_shp, geometry_property=[["area", "AREA_GEODESIC"]], length_unit="", area_unit="SQUARE_KILOMETERS", coordinate_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]", coordinate_format="SAME_AS_INPUT")[0]

        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        Slope_patches2_shp, Long = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Slope_patches1_shp, selection_type="NEW_SELECTION", where_clause="area >= 0.01", invert_where_clause="")

        # Process: Project Raster (2) (Project Raster) (management)
        DEM_Pro_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\DEM_Pro.tif"
        arcpy.management.ProjectRaster(in_raster=DEM_tif, out_raster=DEM_Pro_tif, out_coor_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]", resampling_type="NEAREST", cell_size="35.4428678047127 35.4428678047127", geographic_transform=[], Registration_Point="", in_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", vertical="NO_VERTICAL")
        DEM_Pro_tif = arcpy.Raster(DEM_Pro_tif)

        # Process: Focal Statistics (Focal Statistics) (sa)
        meanDEM_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\MeanDEM.tif"
        Focal_Statistics = meanDEM_tif
        meanDEM_tif = arcpy.sa.FocalStatistics(in_raster=DEM_Pro_tif, neighborhood=Neighbourhood, statistics_type="MEAN", ignore_nodata="DATA", percentile_value=90)
        meanDEM_tif.save(Focal_Statistics)


        # Process: Raster Calculator (Raster Calculator) (sa)
        P_N_Terrains_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\PNTerrains.tif"
        Raster_Calculator = P_N_Terrains_tif
        P_N_Terrains_tif = DEM_Pro_tif -  meanDEM_tif
        P_N_Terrains_tif.save(Raster_Calculator)


        # Process: Reclassify(2) (Reclassify) (3d)
        Negative_Terrains_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Negative Terrains.tif"
        arcpy.ddd.Reclassify(in_raster=P_N_Terrains_tif, reclass_field="VALUE", remap="-1000 0 1;0 1000 NODATA", out_raster=Negative_Terrains_tif, missing_values="NODATA")
        Negative_Terrains_tif = arcpy.Raster(Negative_Terrains_tif)

        # Process: Raster to Polygon(2) (Raster to Polygon) (conversion)
        Negative_Terrains_shp = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Negative Terrains.shp"
        with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
            arcpy.conversion.RasterToPolygon(in_raster=Negative_Terrains_tif, out_polygon_features=Negative_Terrains_shp, simplify="SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

        # Process: Project (Project) (management)
        Negative_Terrains_Pro_shp = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Negative Terrains_Pro.shp"
        arcpy.management.Project(in_dataset=Negative_Terrains_shp, out_dataset=Negative_Terrains_Pro_shp, out_coor_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]", transform_method=[], in_coor_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

        # Process: Feature Class To Feature Class (Feature Class To Feature Class) (conversion)
        Selected_Slope_Patches_1_shp = arcpy.conversion.FeatureClassToFeatureClass(in_features=Slope_patches2_shp, out_path=Output_Location, out_name="坡度斑块筛选2.shp", where_clause="", field_mapping="Id \"Id\" true true false 10 Long 0 10,First,#,坡度斑块筛选1_Layer,Id,-1,-1;gridcode \"gridcode\" true true false 10 Long 0 10,First,#,坡度斑块筛选1_Layer,gridcode,-1,-1;area \"area\" true true false 19 Double 0 0,First,#,坡度斑块筛选1_Layer,area,-1,-1,坡度斑块筛选1_Layer,area,-1,-1", config_keyword="")[0]

        # Process: Intersect (Intersect) (analysis)
        Selected_Slope_Patches_2_shp = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Selected Slope Patches_2 .shp"
        arcpy.analysis.Intersect(in_features=[[Negative_Terrains_Pro_shp, ""], [Selected_Slope_Patches_1_shp, ""]], out_feature_class=Selected_Slope_Patches_2_shp, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")

        # Process: Distance Accumulation (Distance Accumulation) (sa)
        Slope_cost_distance_Ratser_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\result\\Slope Cost Distance.tif"
        Distance_Accumulation = Slope_cost_distance_Ratser_tif
        vertical_raster = ""
        source_direction_raster = ""
        source_location_raster = ""
        with arcpy.EnvManager(parallelProcessingFactor="1"):
            Slope_cost_distance_Ratser_tif = arcpy.sa.DistanceAccumulation(in_source_data=Selected_Slope_Patches_2_shp, in_barrier_data="", in_surface_raster=DEM_tif, in_cost_raster=Slope_tif, in_vertical_raster="", vertical_factor="BINARY 1 -30 30", in_horizontal_raster="", horizontal_factor="BINARY 1 45", out_back_direction_raster=vertical_raster, out_source_direction_raster=source_direction_raster, out_source_location_raster=source_location_raster, source_initial_accumulation="", source_maximum_accumulation="", source_cost_multiplier="", source_direction="", distance_method="PLANAR")
            Slope_cost_distance_Ratser_tif.save(Distance_Accumulation)


        # Process: Reclassify (2) (Reclassify) (3d)
        Reclass_Slope_Cost_Distance_tif: str = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Reclass_Slope Cost Distance.tif"
        arcpy.ddd.Reclassify(in_raster=Slope_cost_distance_Ratser_tif, reclass_field="VALUE", remap="0 1200 1;1200 99999 2", out_raster=Reclass_Slope_Cost_Distance_tif, missing_values="DATA")
        Reclass_Slope_Cost_Distance_tif = arcpy.Raster(Reclass_Slope_Cost_Distance_tif)

        # Process: Focal Statistics (2) (Focal Statistics) (sa)
        Majority_smoothing_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Majority smoothing.tif"
        Focal_Statistics_2_ = Majority_smoothing_tif
        Majority_smoothing_tif = arcpy.sa.FocalStatistics(in_raster=Reclass_Slope_Cost_Distance_tif, neighborhood="Rectangle 3 3 CELL", statistics_type="MAJORITY", ignore_nodata="DATA", percentile_value=90)
        Majority_smoothing_tif.save(Focal_Statistics_2_)


        # Process: Int (Int) (3d)
        Int_tif = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\data\\mid data\\Int_Majority_sm1.tif"
        arcpy.ddd.Int(in_raster_or_constant=Majority_smoothing_tif, out_raster=Int_tif)
        Int_tif = arcpy.Raster(Int_tif)

        # Process: Raster to Polygon (2) (Raster to Polygon) (conversion)
        dune_extraction_shp = "C:\\Users\\WINDOWS\\Desktop\\Dune Extraction\\result\\dune extraction result.shp"
        with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
            arcpy.conversion.RasterToPolygon(in_raster=Int_tif, out_polygon_features=dune_extraction_shp, simplify="SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

        # Process: Calculate Geometry Attributes (2) (Calculate Geometry Attributes) (management)
        dune_extraction_result_shp = arcpy.management.CalculateGeometryAttributes(in_features=dune_extraction_shp, geometry_property=[["area", "AREA_GEODESIC"]], length_unit="", area_unit="SQUARE_KILOMETERS", coordinate_system="PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Mercator_Auxiliary_Sphere\"],PARAMETER[\"False_Easting\",0.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",0.0],PARAMETER[\"Standard_Parallel_1\",0.0],PARAMETER[\"Auxiliary_Sphere_Type\",0.0],UNIT[\"Meter\",1.0]]", coordinate_format="SAME_AS_INPUT")[0]

        # Process: Smooth Shared Edges (Smooth Shared Edges) (cartography)
        Feature, Feature1 = arcpy.cartography.SmoothSharedEdges(in_features=[dune_extraction_result_shp], algorithm="PAEK", tolerance="180 Meters", shared_edge_features=[], in_barriers=[])

if __name__ == '__main__':
    Extraction(*argv[1:])

