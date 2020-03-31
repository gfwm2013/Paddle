#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: define random functions  
# __all__ = ['gaussin', 
#            'uniform', 
#            'shuffle',
#            'randn',
#            'randperm',
#            'rand',
#            'randint']

from __future__ import print_function

import numpy as np
from ..fluid.layer_helper import LayerHelper
from ..fluid.framework import device_guard
from ..fluid.data_feeder import check_type, check_dtype, convert_np_dtype_to_dtype_

__all__ = ['randn']


def randn(shape,
          out=None,
          dtype=None,
          device=None,
          stop_gradient=True,
          name=None):
    """
    This function returns a tensor filled with random numbers from a normal distribution with mean 0 and variance 1 (also called the standard normal
    distribution).

    Args:
        shape(list|tuple): Shape of the generated random tensor.
        out(Variable, optional): Optional output which can be any created Variable that meets the requirements to store the result of operation. If
            the out is `None`, a new Variable wiil be returned to store the result. Default is None.
        dtype(np.dtype|core.VarDesc.VarType|str, optional): Data type of the output tensor, which can be float32, float64.
            if dtype is `None`, the data type of output tensor is `float32`. Default is None.
        device(str, optional): This parameter specifies that the Tensor is created on the GPU or CPU. Default is None.
        stop_gradient(bool, optional): Indicating if we stop gradient from current(out) Variable. Default is True.
        name(str, optional): Normally there is no need for user to set this property. For more information, please refer to :refer:`api_guide_Name` .
            Default is None.

    Returns:
        Random tensor whose data is drawn from a Gaussian distribution, dtype: flaot32 or float64 as specified.

    Return type:
        Variable

    Examples:
        .. code-block:: python

            import paddle.fluid as fluid

            data = fluid.tensor.randn([2, 4])
            exe = fluid.Executor()
            res = exe.run(default_main_program, feed={}, fetch_list=[data])
            print(res[0])
            # array([[2.3060477 , 2.676496  , 3.9911983 , 0.9990833 ],
            #        [2.8675377 , 2.2279181 , 0.79029655, 2.8447366 ]], dtype=float32)

    """
    helper = LayerHelper("randn", **locals())
    check_type(shape, 'shape', (list, tuple), 'randn')
    assert len(shape) > 0, ("The size of argument(shape) can't be zero.")

    if dtype is None:
        dtype = 'float32'

    check_dtype(dtype, 'create data type', ['float32', 'float64'], 'randn')

    if out is None:
        out = helper.create_variable_for_type_inference(dtype=dtype)

    out.stop_gradient = stop_gradient

    dtype = convert_np_dtype_to_dtype_(dtype)
    seed = np.random.randint(0, 100)

    if device is None:
        helper.append_op(
            type='gaussian_random',
            outputs={'Out': out},
            attrs={
                'shape': shape,
                'mean': 0.0,
                'std': 1.0,
                'seed': seed,
                'dtype': dtype,
                'use_mkldnn': False
            })
    else:
        with device_guard(device):
            helper.append_op(
                type='gaussian_random',
                outputs={'Out': out},
                attrs={
                    'shape': shape,
                    'mean': 0.0,
                    'std': 1.0,
                    'seed': seed,
                    'dtype': dtype,
                    'use_mkldnn': False
                })
    return out