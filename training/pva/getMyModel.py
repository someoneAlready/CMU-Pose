#!/usr/bin/python

import os, sys
sys.path.insert(0, '/home/cgangee/code/Realtime_Multi-Person_Pose_Estimation/caffe_train/python')
sys.path.insert(0, '/home/cgangee/code/ohem/tools/')
import _init_paths
import caffe
import google.protobuf.text_format
import google.protobuf as pb


def getModel(src_model, dst_model, src_weights, dst_weights):

    caffe.set_mode_cpu()
    net_src = caffe.Net(src_model, src_weights, caffe.TEST)

    net_dst = caffe.Net(dst_model, caffe.TEST)

    src_keys = net_src.params.keys()
    for key in net_dst.params.keys():

        if key in src_keys:
            src_key = key
        else:
            src_key = '/'.join(key.split('/')[:-1])
            if src_key not in src_keys:
                src_key = None
    
        if src_key != None:
            
            for i in range(len(net_src.params[src_key])):
                if net_dst.params[key][i].data.shape == \
                        net_src.params[src_key][i].data.shape:

                    net_dst.params[key][i].data[:] = \
                            net_src.params[src_key][i].data[:]
        else:
            print(key)

    net_dst.save(dst_weights)



if __name__ == '__main__':
    getModel('original.pt', 'test.pt', 
            'original.model', 'myModel.model')
