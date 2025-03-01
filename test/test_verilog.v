
module test_module (
    input wire in1,
    output wire out1
);
sub_module sub_inst (
    .in_port(in1),
    .out_port(out1)
);
endmodule

module sub_module (
    input wire in_port,
    output wire out_port
);
endmodule
        