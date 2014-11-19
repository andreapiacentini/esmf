# $Id$

"""
This test demonstrates conservative regridding with unstructured meshes.

Two Field objects are created, both on a Mesh.  The source Field is set 
to an analytic function, and a regridding operation is performed from 
the source to the destination Field.  After the regridding is 
completed, the destination Field is compared to the exact solution over
that domain.
"""

try:
    import numpy as np
except:
    raise ImportError('The Numpy library cannot be found!')

try:
    import ESMF
except:
    raise ImportError('The ESMF library cannot be found!')

from ESMF.test.regrid_test.mesh_regridding_utilities import *

esmp = ESMF.Manager(logkind=ESMF.LogKind.MULTI, debug=True)

parallel = False
if ESMF.pet_count() > 1:
    if ESMF.pet_count() > 4:
        raise NameError('MPI rank must be 4 in parallel mode!')
    parallel = True

# opening remarks
if ESMF.local_pet() == 0:
    print "\nmesh_mesh_regrid"

# create two unique Mesh objects
if parallel:
    srcmesh, nodeCoordSrc, nodeOwnerSrc, elemTypeSrc, elemConnSrc = \
        mesh_create_5_parallel()
    dstmesh, nodeCoordDst, nodeOwnerDst, elemTypeDst, elemConnDst = \
        mesh_create_10_parallel()
else:
    srcmesh, nodeCoordSrc, nodeOwnerSrc, elemTypeSrc, elemConnSrc = \
        mesh_create_5()
    dstmesh, nodeCoordDst, nodeOwnerDst, elemTypeDst, elemConnDst = \
        mesh_create_10()

# create ESMP_Field objects on the Meshes
srcfield = ESMF.NewField(srcmesh, 'srcfield', meshloc=ESMF.MeshLoc.ELEMENT)
srcareafield = ESMF.NewField(srcmesh, 'srcareafield', meshloc=ESMF.MeshLoc.ELEMENT)
srcfracfield = ESMF.NewField(srcmesh, 'srcfracfield', meshloc=ESMF.MeshLoc.ELEMENT)
dstfield = ESMF.NewField(dstmesh, 'dstfield', meshloc=ESMF.MeshLoc.ELEMENT)
dstareafield = ESMF.NewField(dstmesh, 'dstareafield', meshloc=ESMF.MeshLoc.ELEMENT)
dstfracfield = ESMF.NewField(dstmesh, 'dstfracfield', meshloc=ESMF.MeshLoc.ELEMENT)
exactfield = ESMF.NewField(dstmesh, 'exactfield', meshloc=ESMF.MeshLoc.ELEMENT)

# initialize the Fields to an analytic function
srcfield = initialize_field_mesh(srcfield, nodeCoordSrc, nodeOwnerSrc, \
                                        elemTypeSrc, elemConnSrc)
exactfield = initialize_field_mesh(exactfield, nodeCoordDst, nodeOwnerDst, \
                                         elemTypeDst, elemConnDst)

# run the ESMF regridding
regridSrc2Dst = ESMF.Regrid(srcfield, dstfield,
                            regrid_method=ESMF.RegridMethod.CONSERVE,
                            unmapped_action=ESMF.UnmappedAction.ERROR, \
                            src_frac_field=srcfracfield, \
                            dst_frac_field=dstfracfield)
dstfield = regridSrc2Dst(srcfield, dstfield)

# compute the mass
srcmass = compute_mass_mesh(srcfield, srcareafield, 
                            dofrac=True, fracfield=srcfracfield)
dstmass = compute_mass_mesh(dstfield, dstareafield)

# compare results and output PASS or FAIL
compare_fields_mesh(dstfield, exactfield, 10E-2, 10E-16, parallel=parallel, 
                    dstfracfield=dstfracfield, mass1=srcmass, mass2=dstmass)