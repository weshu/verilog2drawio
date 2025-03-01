/*

Copyright (c) BalaBala

*/

// Language: Verilog 2001

`resetall
`timescale 1ns / 1ps
`default_nettype none

/*
 * UDP block, IP interface
 */
module udp #
(
    parameter AAAA = 1,
    parameter BBBB = 2048,
    parameter CCCC = 8
)
(
    input  wire        clk,
    input  wire        rst
);

wire        tx_udp_hdr_valid;
wire        tx_udp_hdr_ready;

endmodule

`resetall
