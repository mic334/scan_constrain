%nproc=24
%mem=24GB
#p opt(addredundant) M062X/def2svp scrf=(cpcm,solvent=water) empiricaldispersion=GD3

Title Card Required

1 2
O  0.000000  0.000000  0.117790
H  0.000000  0.676587  -0.409677
H  0.000000  -0.755453  -0.471161

B 1 2 F
X 3 F
X 4 F

