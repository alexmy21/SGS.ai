module hll_3d_cell #(
    parameter NUM_LAYERS = 8,
    parameter HASH_WIDTH = 64
)(
    input [NUM_LAYERS-1:0][HASH_WIDTH-1:0] layer_registers,
    output [NUM_LAYERS-1:0][NUM_LAYERS-1:0] vertical_entanglement
);
    genvar z, zz;
    generate
        for (z = 0; z < NUM_LAYERS; z = z + 1) begin : layer_z
            for (zz = 0; zz < NUM_LAYERS; zz = zz + 1) begin : layer_zz
                if (z != zz) begin
                    assign vertical_entanglement[z][zz] = 
                        (layer_registers[z] & layer_registers[zz]) != 0;
                end else begin
                    assign vertical_entanglement[z][zz] = 0; // No self-entanglement
                end
            end
        end
    endgenerate
endmodule