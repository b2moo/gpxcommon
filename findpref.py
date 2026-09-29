#!./bin/python3

import sys
import gpxpy
from geopy.distance import geodesic

def charger_gpx(fichier):
    """Charge un fichier GPX et retourne la liste des points de la première trace."""
    with open(fichier, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    
    # On prend la première trace et le premier segment
    if gpx.tracks:
        trace = gpx.tracks[0]
        if trace.segments:
            return [(point.latitude, point.longitude) for point in trace.segments[0].points]
    return []

def parcours_commun_debut(fichier1, fichier2, tolerance_metres=50):
    """
    Trouve le début du parcours en commun entre deux fichiers GPX.

    Args:
        fichier1: Chemin vers le premier fichier GPX
        fichier2: Chemin vers le deuxième fichier GPX
        tolerance_metres: Tolérance en mètres pour considérer que deux points sont identiques

    Returns:
        Liste des points du parcours commun au début
    """
    points1 = charger_gpx(fichier1)
    points2 = charger_gpx(fichier2)

    if not points1 or not points2:
        return []

    commun = []
    min_length = min(len(points1), len(points2))

    for i in range(min_length):
        dist = geodesic(points1[i], points2[i]).meters
        if dist <= tolerance_metres:
            commun.append(points1[i])
        else:
            break

    return commun

def sauvegarder_gpx(points, fichier_sortie):
    """Sauvegarde une liste de points dans un fichier GPX."""
    gpx = gpxpy.gpx.GPX()

    # Créer une trace avec un segment
    trace = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(trace)
    segment = gpxpy.gpx.GPXTrackSegment()
    trace.segments.append(segment)

    for lat, lon in points:
        segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))

    with open(fichier_sortie, 'w') as f:
        f.write(gpx.to_xml())

# Exemple d'utilisation
if __name__ == "__main__":
    fichier1 = sys.argv[1]
    fichier2 = sys.argv[2]
    fichier_sortie = sys.argv[3]

    points_communs = parcours_commun_debut(fichier1, fichier2)

    if points_communs:
        print(f"Trouvé {len(points_communs)} points communs au début des parcours")
        sauvegarder_gpx(points_communs, fichier_sortie)
        print(f"Parcours commun sauvegardé dans {fichier_sortie}")
    else:
        print("Aucun parcours commun trouvé au début des fichiers")
