`timescale 1ns / 1ps

module baseline_non_sc(
    input logic clk,
    input logic rst_n,
    input logic [7:0] r_in,
    input logic [7:0] g_in,
    input logic [7:0] b_in,
    output logic [7:0] r_out,
    output logic [7:0] g_out,
    output logic [7:0] b_out,
    output logic done
    );
    
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_out <= '0;
            g_out <= '0;
            b_out <= '0;
            done <= '0;
        end else begin
            r_out <= ({8'd0, r_in} * {8'd0, r_in}) >> 8;
            g_out <= ({8'd0, g_in} * {8'd0, g_in}) >> 8;
            b_out <= ({8'd0, b_in} * {8'd0, b_in}) >> 8;
            done <= '1;
        end
    end
endmodule
