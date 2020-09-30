import math
import random

import pyglet

from engine.Antibody import Antibody
from engine.Antigen import Antigen
from engine.Colors import Colors
from engine.CuboidFactory import CuboidFactory
from engine.EllipsoidFactory import EllipsoidFactory
from quadtree.Quadtree import Quadtree
from quadtree.Rectangle import Rectangle
from utils.Point2D import Point2D
from utils.Point3D import Point3D


def check_collision_sorted_collection(antibody, collection):
    distance = distance_from_origin(antibody)
    r = 2 * max(antibody.a, antibody.b)

    antibodies = collection.find_between_range(distance - r, distance + r)
    box_new_antibody = antibody.box
    for ab in antibodies:
        box_ab = ab.box
        found = box_new_antibody.collides(box_ab)
        if found:
            return True
    return False


def distance_from_origin(antibody):
    return math.sqrt(antibody.center_point.x ** 2 + antibody.center_point.z ** 2)


def check_collision_antibodies(object_1, antibodies):
    for antibody in antibodies:
        if object_1.box.overlaps(antibody.box):
            return True
    return False


def check_collision_antigens(antigen, antigens):
    for anti in antigens:
        if antigen.overlaps_with_antigen(anti):
            return True
    return False


class Renderer:
    def __init__(self, user_input):
        self.batch = pyglet.graphics.Batch()
        self.colors = Colors()
        self.create_antibodies = self.create_antibodies_fab_up
        self.user_input = user_input
        self.radius_antibody = user_input['diameter_antibody'] / 2
        self.half_height_antibody = user_input['height_antibody'] / 2
        self.width_surface = user_input['width_surface']
        self.half_width_surface = self.width_surface / 2
        if user_input['method'] == 'side_on':
            self.create_antibodies = self.create_antibodies_side_on
        if user_input['method'] == 'random':
            self.distance_between_points = user_input['distance_between_points']
            self.create_antibodies = self.create_antibodies_random
            self.number_of_antibodies = self.calculate_number_of_antibodies(user_input['ratio_antibodies'])
            self.probability_antibody_flat_on = user_input['probability_antibody_flat_on']
        self.surface_point = Point3D(0, 0, 0)
        self.surface_center_point = Point2D(self.surface_point.x + self.half_width_surface,
                                            self.surface_point.z + self.half_width_surface)
        self.height_surface = 2
        self.radius_antigen = user_input['radius_antigen']
        self.boundary_surface = Rectangle(self.surface_center_point, self.half_width_surface, self.half_width_surface)
        self.tree_antibodies = Quadtree(self.boundary_surface, 4)
        self.tree_antigens = Quadtree(self.boundary_surface, 4)

    def calculate_number_of_antibodies(self, ratio):
        avogadro_number = 6.022 * (10 ** 23)
        n_mol = ratio / 150000
        mol = n_mol * 0.000000001
        molecules_cm_squared = avogadro_number * mol
        molecules_micrometer_squared = molecules_cm_squared / 100000000
        area_surface = self.width_surface ** 2
        molecules_on_surface = (molecules_micrometer_squared * area_surface) / 1000000
        print("Massimo numero di anticorpi sulla superficie:", int(molecules_on_surface))
        return int(molecules_on_surface)

    def add_models_to_batch(self, models):
        for model in models:
            self.batch.add(model.count, model.mode, model.group, model.verteces, model.color)

    def draw_batch(self):
        self.batch.draw()

    def create_surface(self):
        factory = CuboidFactory()
        surface = factory.get_models(self.surface_point.x, self.surface_point.y, self.surface_point.z,
                                     self.width_surface, self.height_surface, self.colors.surface_colors)
        self.add_models_to_batch(surface)

    def draw_antibody(self, antibody):
        factory = EllipsoidFactory()
        x = antibody.center_point.x
        y = antibody.center_point.y
        z = antibody.center_point.z
        if antibody.orientation == 4:
            color = self.colors.yellow
        else:
            color = self.colors.black
        ellipsoid, vertices = factory.get_models(x, y + antibody.c, z, antibody.a, antibody.b, antibody.c, color,
                                                 antibody.theta)
        antibody.vertices_3d = vertices
        self.add_models_to_batch(ellipsoid)

    def draw_antigen(self, antigen):
        factory = EllipsoidFactory()
        x = antigen.center_point.x
        y = antigen.center_point.y
        z = antigen.center_point.z
        color = self.colors.purple
        sphere, vertices = factory.get_models(x, y, z, antigen.radius, antigen.radius, antigen.radius, color, 0)
        self.add_models_to_batch(sphere)

    def is_antibody_flat_on(self):
        # 0 -> sdraiato, 1 -> in piedi
        r = random.choices([0, 1], weights=[self.probability_antibody_flat_on, 1 - self.probability_antibody_flat_on],
                           k=1)
        return r.pop() == 0

    # Genero tutti gli anticorpi sdraiati "uno dopo l'altro"
    def create_antibodies_flat_on(self):
        flat_on = 0
        center_point = Point3D(self.radius_antibody, float(self.surface_point.y + self.height_surface),
                               self.radius_antibody)
        while center_point.x < (self.width_surface - self.radius_antibody):
            while center_point.z < (self.width_surface - self.radius_antibody):
                antibody = Antibody(4, center_point, self.radius_antibody, self.radius_antibody,
                                    self.half_height_antibody, 0)
                self.draw_antibody(antibody)
                self.tree_antibodies.insert(antibody)
                flat_on += 1
                center_point.z = center_point.z + 2 * self.radius_antibody
                print("Anticorpo n: ", flat_on)
            center_point.z = self.radius_antibody
            center_point.x = center_point.x + 2 * self.radius_antibody

    # Genero tutti gli anticorpi in piedi "uno dopo l'altro"
    def create_antibodies_fab_up(self):
        fab_up = 0
        center_point = Point3D(self.radius_antibody, float(self.surface_point.y + self.height_surface),
                               self.half_height_antibody)
        while center_point.x < (self.width_surface - self.radius_antibody):
            while center_point.z < (self.width_surface - self.half_height_antibody):
                antibody = Antibody(1, center_point, self.half_height_antibody, self.radius_antibody,
                                    self.radius_antibody, math.radians(90))
                self.draw_antibody(antibody)
                self.tree_antibodies.insert(antibody)
                fab_up += 1
                center_point.z = center_point.z + 2 * self.half_height_antibody
                print("Anticorpo n: ", fab_up)
            center_point.z = self.half_height_antibody
            center_point.x = center_point.x + 2 * self.radius_antibody

    def create_antibodies_side_on(self):
        side_on = 0
        center_point = Point3D(self.radius_antibody, float(self.surface_point.y + self.height_surface),
                               self.half_height_antibody)
        while center_point.x < (self.width_surface - self.radius_antibody):
            while center_point.z < (self.width_surface - self.half_height_antibody):
                antibody = Antibody(3, center_point, self.half_height_antibody, self.radius_antibody,
                                    self.radius_antibody, math.radians(90))
                self.draw_antibody(antibody)
                self.tree_antibodies.insert(antibody)
                side_on += 1
                center_point.z = center_point.z + 2 * self.half_height_antibody
                print("Anticorpo n: ", side_on)
            center_point.z = self.half_height_antibody
            center_point.x = center_point.x + 2 * self.radius_antibody

    def get_center_points_within_surface(self, step):
        half_step = step / 2
        center_points = []
        i = 0
        j = 0
        while i < self.width_surface:
            while j < self.width_surface:
                center_point = Point3D(j + half_step, float(self.surface_point.y + self.height_surface), i + half_step)
                center_points.append(center_point)
                j += step
            j = 0
            i += step
        return center_points

    def create_antibodies_random(self):
        sdraiati = 0
        in_piedi = 0
        # step = 2 * min(self.radius_antibody, self.half_height_antibody)
        step = self.distance_between_points
        if step == 0:
            step = 0.1
        center_points = self.get_center_points_within_surface(step)
        random.shuffle(center_points)
        for center_point in center_points:
            if sdraiati + in_piedi == self.number_of_antibodies:
                break
            center_point_2d = Point2D(center_point.x, center_point.z)
            width_square = 2 * max(self.radius_antibody, self.half_height_antibody)
            square = Rectangle(center_point_2d, width_square, width_square)
            antibodies = self.tree_antibodies.query(square, [])
            if self.is_antibody_flat_on():
                antibody = Antibody(4, center_point, self.radius_antibody, self.radius_antibody,
                                    self.half_height_antibody, 0)
                if not self.boundary_surface.completely_contains_polygon(antibody.box.vertices):
                    continue
                if not check_collision_antibodies(antibody, antibodies):
                    if self.tree_antibodies.insert(antibody):
                        self.draw_antibody(antibody)
                        sdraiati += 1
                        print("Anticorpo n: ", in_piedi + sdraiati)
            else:
                orientation = random.randint(1, 3)  # Scelgo un orientamento casuale tra fab-up, fab-down e side on
                thetas = [0.0, 22.5, 45.0, 67.5, 90.0, 112.5, 135.0, 157.5]
                random.shuffle(thetas)
                for theta in thetas:
                    antibody = Antibody(orientation, center_point, self.half_height_antibody, self.radius_antibody,
                                        self.radius_antibody, math.radians(theta))
                    if not self.boundary_surface.completely_contains_polygon(antibody.box.vertices):
                        continue
                    if not check_collision_antibodies(antibody, antibodies):
                        if self.tree_antibodies.insert(antibody):
                            self.draw_antibody(antibody)
                            in_piedi += 1
                            print("Anticorpo n: ", in_piedi + sdraiati)
                            break

    def get_random_point_2d_within_surface(self):
        x = random.uniform(self.surface_point.x, self.surface_point.x + self.width_surface)
        y = random.uniform(self.surface_point.z, self.surface_point.z + self.width_surface)
        return Point2D(x, y)

    def create_antigens(self):
        count = 0
        tries = 0
        while tries < 1000:
            tries += 1
            center_point_2d = self.get_random_point_2d_within_surface()
            antigen = Antigen(Point3D(center_point_2d.x, 0, center_point_2d.y), self.radius_antigen)
            if not self.boundary_surface.completely_contains_polygon(antigen.box.vertices):
                continue
            width_big_quare = 2 * max(self.radius_antibody, self.half_height_antibody)
            big_square = Rectangle(center_point_2d, width_big_quare, width_big_quare)
            antibodies = self.tree_antibodies.query(big_square, [])
            if len(antibodies) == 0:
                continue
            vertices = []
            for antibody in antibodies:
                if antigen.box.overlaps(antibody.box):
                    for v in antibody.vertices_3d:
                        v_2d = Point2D(v.x, v.z)
                        if center_point_2d.distance_squared(v_2d) <= antigen.radius ** 2:
                            vertices.append(v)
            if len(vertices) == 0:
                continue
            vertices.sort(key=lambda x: x.y, reverse=True)
            center_point = Point3D(center_point_2d.x, vertices[0].y, center_point_2d.y)
            antigen = Antigen(center_point, self.radius_antigen)
            step = 0.05
            last_vertex = None
            while len(vertices) > 0:
                v = vertices[0]
                if antigen.contains(v):
                    antigen.center_point.y += step
                    last_vertex = v
                else:
                    vertices.remove(v)

            if last_vertex is None:
                continue
            ab = None
            for antibody in antibodies:
                if last_vertex in antibody.vertices_3d:
                    ab = antibody
            if ab.empty_antigen_binding_sites == 0:
                continue
            if antigen.center_point.y - self.radius_antigen < self.height_surface:
                continue
            small_square = Rectangle(center_point_2d, 2 * self.radius_antigen, 2 * self.radius_antigen)
            antigens = self.tree_antigens.query(small_square, [])
            if check_collision_antigens(antigen, antigens):
                continue
            ab.empty_antigen_binding_sites -= 1
            self.draw_antigen(antigen)
            self.tree_antigens.insert(antigen)
            count += 1
            # Sono riuscito a mettere l'antigene, allora azzero il contatore dei tentativi
            tries = 0
            print("Antigene n: ", count)
        print("FINITO")

    def get_data(self):
        antibodies = self.tree_antibodies.query(self.boundary_surface, [])
        antigens = self.tree_antigens.query(self.boundary_surface, [])
        number_of_antibodies = len(antibodies)
        number_of_antigens = len(antigens)
        fab_up = 0
        fab_down = 0
        side_on = 0
        flat_on = 0
        for ab in antibodies:
            if ab.orientation == 1:
                fab_up += 1
            elif ab.orientation == 2:
                fab_down += 1
            elif ab.orientation == 3:
                side_on += 1
            else:
                flat_on += 1
        binding_sites = 2 * fab_up + side_on
        if binding_sites != 0:
            antigens_over_binding_sites = round((number_of_antigens / binding_sites), 4)
        else:
            antigens_over_binding_sites = None
        output = {'number_of_antibodies': number_of_antibodies,
                  'antibodies_flat_on': flat_on,
                  'antibodies_side_on': side_on,
                  'antibodies_fab_down': fab_down,
                  'antibodies_fab_up': fab_up,
                  'number_of_antigens': number_of_antigens,
                  'number_of_binding_sites': binding_sites,
                  'antigens_over_binding_sites': antigens_over_binding_sites}

        data = {'input': self.user_input.copy(), 'output': output}
        return data


"""
    def create_antibodies(self):
        boundary = Rectangle(self.surface_center_point, self.half_width_surface, self.half_width_surface)
        tree = Quadtree(boundary, 4)
        sdraiati = 0
        in_piedi = 0
        step = 2 * self.half_height_antibody
        half_step = step / 2
        i = 0
        j = 0
        while i < self.width_surface:
            while j < self.width_surface:
                center_point = Point3D(j + half_step, float(self.surface_point.y + self.height_surface), i + half_step)
                antibody = Antibody(4, center_point, self.radius_antibody, self.radius_antibody,
                                    self.half_height_antibody, 0)
                if not boundary.completely_contains_polygon(antibody.box.vertices):
                    j += step
                    continue
                center_point_2d = Point2D(antibody.center_point.x, antibody.center_point.z)
                rectangle = Rectangle(center_point_2d, 2 * max(antibody.a, antibody.b), 2 * max(antibody.a, antibody.b))
                antibodies = tree.query(rectangle, [])
                if is_antibody_flat_on():
                    if not check_collision(antibody, antibodies):
                        if tree.insert(antibody):
                            # print_points(antibody.box.vertices)
                            self.draw_antibody(antibody)
                            sdraiati += 1
                            print("Anticorpo n: ", in_piedi + sdraiati)
                else:
                    thetas = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5]
                    while len(thetas) > 0:
                        theta = thetas[randint(0, len(thetas)) - 1]
                        thetas.remove(theta)
                        antibody = Antibody(1, center_point, self.half_height_antibody, self.radius_antibody,
                                            self.radius_antibody, math.radians(theta))
                        if not check_collision(antibody, antibodies):
                            if tree.insert(antibody):
                                # print_points(antibody.box.vertices)
                                self.draw_antibody(antibody)
                                in_piedi += 1
                                print("Anticorpo n: ", in_piedi + sdraiati)
                                break
                j += step
            j = 0
            i += step
        print("Anticorpi sdraiati: ", sdraiati, "Anticorpi in piedi: ", in_piedi)
"""
