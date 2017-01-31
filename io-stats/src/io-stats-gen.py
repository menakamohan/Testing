#!/usr/bin/python

import sys
from generator import ops, fop_subs, cbk_subs, generate

#   FOPs that are not the part of the below list are,
#   -mkdir
#   -open
#   -create
#   -readv
#   -writev
#   -readdirp
#   -setxattr
#   -opendir
fop_table = {'stat', 'readlink', 'mknod', 'unlink', 'rmdir', 'symlink',
        'rename', 'link', 'truncate', 'statfs', 'flush', 'fsync', 'getxattr',
        'removexattr', 'fsetxattr', 'fgetxattr', 'fremovexattr',
        'readdir', 'fsyncdir', 'access', 'ftruncate', 'fstat', 'lk',
        'inodelk', 'finodelk', 'entrylk', 'fentrylk', 'lookup', 'xattrop', 'fxattrop',
        'setattr', 'fsetattr', 'fallocate', 'discard', 'zerofill', 'ipc', 'rchecksum',
        'seek', 'lease', 'getactivelk', 'setactivelk', 'compound'}

OP_CBK_TEMPLATE = """
int
io_stats_@NAME@_cbk (call_frame_t *frame, void *cookie, xlator_t *this,
                     int32_t op_ret, int32_t op_errno,
                     @LONG_ARGS@)
{

        UPDATE_PROFILE_STATS (frame, @NAME@);
        STACK_UNWIND_STRICT (@NAME@, frame, op_ret, op_errno,
                             @SHORT_ARGS@);
        return 0;
}
"""

OP_FOP_TEMPLATE = """
int
io_stats_@NAME@ (call_frame_t *frame, xlator_t *this,
                 @LONG_ARGS@)
{
        START_FOP_LATENCY (frame);

        STACK_WIND (frame, io_stats_@NAME@_cbk,
                    FIRST_CHILD (this),
                    FIRST_CHILD (this)->fops->@NAME@,
                    @SHORT_ARGS@);
        return 0;
}
"""

def gen_defaults ():
    for name in fop_table:
        print name
        print generate(OP_CBK_TEMPLATE,name,cbk_subs)
        print generate(OP_FOP_TEMPLATE,name,fop_subs)

for l in open(sys.argv[1],'r').readlines():
	if l.find('#pragma generate') != -1:
		print "/* BEGIN GENERATED CODE - DO NOT MODIFY */"
		gen_defaults()
		print "/* END GENERATED CODE */"
	else:
		print l[:-1]


