module port_declaration_test;

    // Single - bit port declarations without wire/reg keyword
    input clk;
    output valid;
    inout io_single;

    // Single - bit port declarations with wire keyword
    input wire rst;
    output wire data_ready;
    inout wire io_wire;

    // Single - bit port declarations with reg keyword
    input reg sync_signal;
    output reg data_out;

    // Multi - bit port declarations
    input [7:0] data_in_8bit;
    output [15:0] data_out_16bit;
    inout [3:0] io_4bit;

    // Multi - bit port declarations with wire keyword
    input wire [23:0] data_in_24bit_wire;
    output wire [31:0] data_out_31bit_wire;
    inout wire [1:0] io_2bit_wire;

    // Multi - bit port declarations with reg keyword
    input reg [63:0] data_in_64bit_reg;
    output reg [47:0] data_out_47bit_reg;

    // Signed port declarations
    input signed [15:0] signed_data_in;
    output signed [23:0] signed_data_out;
    inout signed [7:0] signed_io;

    // Signed multi - bit port declarations with wire keyword
    input wire signed [31:0] signed_data_in_31bit_wire;
    output wire signed [11:0] signed_data_out_11bit_wire;
    inout wire signed [5:0] signed_io_5bit_wire;

    // Signed multi - bit port declarations with reg keyword
    input reg signed [47:0] signed_data_in_47bit_reg;
    output reg signed [19:0] signed_data_out_19bit_reg;


endmodule