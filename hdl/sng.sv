`timescale 1ns / 1ps
// stochastic number bitstream generator

module sng (
  input logic [7:0] num_in,
  input logic [7:0] lfsr_in,
  output logic bitstream
);
  assign bitstream = (num_in > lfsr_in);
endmodule