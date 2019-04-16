'''
Created on January 12, 2015

@author: Robert PASTOR

verify that ground run length varies with aircraft mass

'''


from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase


if __name__ == '__main__':

    print ( '=========== main start ==================' )
    aircraftIcaoCode = 'A320'

    atmosphere = Atmosphere()
    assert (not(atmosphere is None))
    
    earth = Earth()
    assert (not(earth is None))

    acBd = BadaAircraftDatabase()
    assert acBd.read()
        
    if ( acBd.aircraftExists(aircraftIcaoCode) 
             and acBd.aircraftPerformanceFileExists(aircraftIcaoCode)):
            
            aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
            aircraft.dump()
    else:
        raise ValueError(': aircraft not found= ' + aircraftIcaoCode)

    assert not(aircraft is None)
    
    print ( '================ load airports =================' )
    airportsDB = AirportsDatabase()
    assert (airportsDB.read())
    
    adepIcaoCode = 'LFML'

    departureAirport = airportsDB.getAirportFromICAOCode(adepIcaoCode)
    print ( ': departure airport= ' + str(departureAirport) )
    assert not (departureAirport is None)
    
    print ( '================ load runways =================' )

    runWaysDatabase = RunWayDataBase()
    assert (runWaysDatabase.read())

    print ( '====================  take off run-way ==================== ' )
    departureRunway = runWaysDatabase.getFilteredRunWays(adepIcaoCode, 
                                                         'TakeOff', 
                                                         aircraft.WakeTurbulenceCategory)
    print ( '=========== minimum and maximum aircraft mass ==================' )

    minMassKg = aircraft.getMinimumMassKilograms()
    print ( 'aircraft minimum mass: ' + str(minMassKg) + ' kilograms' )
    
    maxMassKg = aircraft.getMaximumMassKilograms()
    print ( 'aircraft maximum mass: ' + str(maxMassKg) + ' kilograms' )

    deltaMass = maxMassKg - minMassKg
    massKg = 39000.0
    while (massKg < maxMassKg):
        
        massKg += 1000.0
        print ( '==================== set aircraft reference mass ==================== ' )
        aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
        
        aircraft.setTargetCruiseFlightLevel(310, departureAirport.getFieldElevationAboveSeaLevelMeters())
        
        print ( '==================== aircraft reference mass ==================== ' )
        print ( 'aircraft reference mass= ' + str(massKg) + ' Kilograms' )
        
        aircraft.setAircraftMassKilograms(massKg)
        print ( '==================== begin of ground run ==================== ' )
        groundRunLeg = GroundRunLeg(runway = departureRunway, 
                                     aircraft = aircraft,
                                     airport = departureAirport)
        groundRunLeg.buildDepartureGroundRun(elapsedTimeSeconds = 0.0, 
                                             distanceStillToFlyMeters = 500000.0)
        #groundRunLeg.createXlsxOutputFile()
        print ( '==================== end of ground run ==================== ' )
        initialWayPoint = groundRunLeg.getLastVertex().getWeight()
            
        print ( '==================== dump aircraft speed profile ==================== ' )
        aircraft.createStateVectorOutputFile()
        print ( '=========== main end ==================' )
