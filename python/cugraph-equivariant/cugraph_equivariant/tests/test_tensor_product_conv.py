# Copyright (c) 2024, NVIDIA CORPORATION.
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

import pytest
import torch

def test_tensor_product_conv_equivariance(
        create_tp_conv_and_data, 
):
    torch.manual_seed(12345)

    (tp_conv,
     (src_features, edge_sh, edge_emb, edge_index, num_dst_nodes, src_scalars, dst_scalars),
     (D_in, D_sh, D_out)
     ) = create_tp_conv_and_data
    
    # rotate before
    out_before = tp_conv(
        src_features=src_features @ D_in.T,
        edge_sh=edge_sh @ D_sh.T,
        edge_emb=edge_emb,
        edge_index=edge_index,
        num_dst_nodes=num_dst_nodes,
        src_scalars=src_scalars,
        dst_scalars=dst_scalars,
    )

    # rotate after
    out_after = (
        tp_conv(
            src_features=src_features,
            edge_sh=edge_sh,
            edge_emb=edge_emb,
            edge_index=edge_index,
            num_dst_nodes=num_dst_nodes,
            src_scalars=src_scalars,
            dst_scalars=dst_scalars,
        )
        @ D_out.T
    )

    torch.allclose(out_before, out_after, rtol=1e-4, atol=1e-4)
