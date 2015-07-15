%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Environment setup
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 belongs_to(a0, r1).
 belongs_to(a1, r1).
 belongs_to(a2, r1).

 belongs_to(r1,f1).
 belongs_to(f1,b1).

 is_connected(d1, r1).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Testing / Scenarios
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%  Initial location of robot 
holds(has_location(rob0, a0), 0).

%% Initial scene description
%% holds(has_state(d1, closed), 0).

has_size(block0, small).
has_colour(block0, blue).
has_shape(block0, cuboid).
has_surface(block0, s0).

has_size(block1, small).
has_colour(block1, red).
has_shape(block1, prism).
has_surface(block1, s1).

has_size(block2, small).
has_colour(block2, blue).
has_shape(block2, cube).
has_surface(block2, s2).

has_size(block3, small).
has_colour(block3, red).
has_shape(block3, cube).
has_surface(block3, s3).


has_size(block4, small).
has_colour(block4, yellow).
has_shape(block4, prism).
has_surface(block4, s4).

has_surface(tab0, s5).

%% Initial location of table and blocks
holds(has_location(tab0, a0), 0).
holds(on(block0, s5), 0).
holds(on(block1, s2), 0).
holds(on(block2, s5), 0).
holds(on(block3, s5), 0).
holds(on(block4, s5), 0).